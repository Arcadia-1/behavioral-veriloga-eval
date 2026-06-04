# 083 Record Node-ID Rust ABI

## 核心结论

这一轮把 B15 record path 中的 recorded-node value gather 迁到 Rust：

```text
recorded signal names
-> precomputed node ids
-> Rust gathers node_values[node_id]
-> Python appends values to SimResult trace
```

它不是某个 benchmark 的特化逻辑，而是所有 indexed-array trace 都能复用的通用 runtime primitive。默认非 indexed 路径不变；如果 Rust backend 不可用或调用失败，会 fallback 到原 Python `IndexedVoltageArray.values_for_ids()`。

## 改造原理

record 本身不涉及复杂数学，慢点主要来自 Python 每个 record point 的小对象循环：

```text
for recorded_node_id in ids:
    values.append(indexed_values[recorded_node_id])
```

这轮改成 Rust array loop：

```text
for i in 0..node_ids.len():
    out[i] = values[node_ids[i]]
```

这类操作的特点是：

- 数据已经是 contiguous indexed voltage array；
- node name 到 node id 已经预计算；
- Rust 可以直接按 `usize` id 读取 `f64` array；
- 越界 node id 按 Python 旧语义返回 default，不 panic。

所以它适合做成全局 primitive，而不是继续针对 SAR/CPPLL/prop-delay 之类写特殊 trace copy。

## 改动内容

| 文件 | 改动 |
|---|---|
| `EVAS/evas/rust_core/src/lib.rs` | 新增 `record_values_for_node_ids()` 和 C ABI `evas_rust_record_values_for_node_ids()` |
| `EVAS/evas/simulator/rust_backend.py` | 新增 `RustBackend.record_values_for_ids()` wrapper |
| `EVAS/evas/simulator/engine.py` | indexed array loop 启用时，为 recorded nodes 建立 `RustNodeIdBatch`，record point 优先走 Rust gather |
| `EVAS/tests/test_rust_backend.py` | 覆盖 Python wrapper 的 node-id gather 和 default 行为 |
| `EVAS/tests/test_engine.py` | 覆盖 80-node indexed trace 下 Rust record scan 与默认 waveform parity |
| `behavior-coverage-map.v1.json` | B15 记录 Rust primitive，移除 `rust_record_abi_not_implemented` blocker |

## 正确性边界

这轮只迁移 value gather，不迁移下面这些外层行为：

| 行为 | 当前状态 |
|---|---|
| `self.time_points.append(time)` | Python |
| `recorded_signals[name].append(value)` | Python |
| `SimResult` assembly | Python |
| CSV 写出 | Python/harness |
| checker required-signal contract | Python/harness |

也就是说，B15 从“没有 Rust record ABI”变成“record value gather 有 Rust ABI”，但还不能说整个 trace/CSV/checker pipeline 已全 Rust 化。

## 验证结果

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m py_compile \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/simulator/engine.py \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/simulator/rust_backend.py
PASS
```

```text
cargo test --manifest-path /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/rust_core/Cargo.toml records_values --release
PASS
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_rust_backend.py \
  -k "record_values or max_err_ratio" -q
PASS
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_engine.py \
  -k "indexed_arrays_use_rust_record_scan or indexed_arrays_preserve_source_record" -q
PASS
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests -q
561 passed
```

## 速度影响判断

这次减少的是每个 record point 上的 Python node-id gather 开销。它对下面情况更有意义：

- recorded signals 很多；
- record point 很密；
- indexed array loop 已经启用；
- Rust whole-segment path 生成了大量 node array values，需要快速抽取 checker 必需列。

它对只有一两个 recorded signal 的小 row 收益会很小，因为 Python list append、CSV 写出和 checker 外层仍会占主要时间。

## 下一步

1. 把 record append 从 Python `list.append` 迁到 preallocated trace matrix，减少 per-point object append。
2. 将 whole-segment Rust trace 的输出统一复用 B15 record ABI，避免每个 fastpath 自己维护 record copy。
3. 再推进 event queue 级 Rust segment：multi timer ordering、cross/above interpolation、transition state/output record。
