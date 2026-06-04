# 054 - Dynamic Bus Offset Rust Primitive

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `019-dynamic-bus-lowering-prototype.md`
- `023-dynamic-bus-runtime-codegen-fix.md`
- `049-behavior-coverage-manifest.md`
- `../behavior-coverage-map.v1.json`

## One-Line Summary

为 B17 dynamic bus / hierarchy resolution 增加 Rust base+offset primitive：`evas_rust_dynamic_bus_offsets` 可以对 bounded 1-D/2-D bus access 计算 node-id，带负 index、越界和 overflow 检查；当前 compiler/runtime 生产路径仍使用 Python `_resolve_dynamic_node()` 字符串 cache。

## Why This Exists

动态 bus 的慢点来自两类操作：

```text
1. 每步把 V(bus[i]) 格式化成 "bus[3]" 这类字符串
2. 再用字符串 node name 走 dict/cache/output writer
```

Rust/native backend 不应该在 hot loop 里构造字符串。更合理的形态是：

```text
base_node_id + index * stride + optional_second_index -> node_id
node_values[node_id]
```

054 先把这个数学核心做成 Rust primitive。这样后续 compiler 只要能提供 `base_offset / outer_len / inner_stride / inner_len / index`，就能绕开字符串节点名。

## Changed Code

| Area | File | Change |
|---|---|---|
| Rust core | `EVAS/evas/rust_core/src/lib.rs` | 新增 `dynamic_bus_offsets_for_arrays` 和 C ABI `evas_rust_dynamic_bus_offsets` |
| Python bridge | `EVAS/evas/simulator/rust_backend.py` | 新增 optional ctypes binding `RustBackend.dynamic_bus_offsets` |
| Tests | `EVAS/tests/test_rust_backend.py` | 验证 1-D/2-D offset 计算和 out-of-bounds error wrapping |
| Manifest | `behavior-coverage-map.v1.json` | B17 从 `python_only` 更新为 `partial` |

## Math

1-D bus:

```text
node_id = base_offset + i
```

2-D bus with row-major layout:

```text
node_id = base_offset + i * inner_stride + j
```

边界条件：

```text
0 <= i < outer_length
0 <= j < inner_length  only when second index exists
```

这只是 node-id 计算，不包含 Verilog-A index expression evaluation。`i` 和 `j` 仍需要 Python/compiler/Rust evaluate IR 先算出来。

## What Is Still Python-Owned

| Remaining piece | Status |
|---|---|
| dynamic index expression evaluation | still Python unless the expression was already lowered elsewhere |
| `_resolve_dynamic_node()` string cache | still production path |
| compiler lowering from declared bus ranges to base offsets | not wired |
| child-model / `@parent:` hierarchy mapping | still Python node map |
| output writer / record schema | unchanged |

## Verification

Fresh checks:

```text
cargo test
25 passed

cargo build --release
passed

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_rust_backend.py -q
18 passed
```

## Claim Boundary

This is not full B17 production Rust. It is the arithmetic primitive needed by a future typed dynamic-bus backend. Current user-visible dynamic bus behavior still comes from Python codegen and `_resolve_dynamic_node()`.
