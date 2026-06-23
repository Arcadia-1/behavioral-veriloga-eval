# 052 - Cross/Above Detector Rust Primitives

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `049-behavior-coverage-manifest.md`
- `051-timer-step-rust-primitives.md`
- `../behavior-coverage-map.v1.json`

## One-Line Summary

为 B09 `cross()` / `above()` 事件检测增加 Rust typed-array primitive，并用 Python `CrossDetector` / `AboveDetector` 作为 oracle 做 ctypes parity；当前仍不接管 event body、event ordering、crossing-time interpolation side effects。

## Why This Exists

事件驱动仿真的慢点不是单独一个函数，而是这条链：

```text
读表达式 -> 检测 crossing/above -> 计算 event time -> 设置插值上下文 -> 执行 event body -> 刷新输出 -> 影响下一步 dt/refine
```

这次只迁移中间的“检测器状态更新”：

```text
上一时刻值 + 当前值 + 方向 + 容差
  -> 是否触发 + crossing time + detector 下一状态
```

它是纯数组计算，适合 Rust；但 event body 会改 `self.state`、`output_nodes`、timer/transition state，并且多个事件在同一步内还有时间顺序要求，所以不能直接把 B09 宣称为 production Rust。

## Changed Code

| Area | File | Change |
|---|---|---|
| Rust core | `EVAS/evas/rust_core/src/lib.rs` | 新增 `cross_detector_step_for_arrays` / `above_detector_step_for_arrays` 和 C ABI `evas_rust_cross_detector_step` / `evas_rust_above_detector_step` |
| Python bridge | `EVAS/evas/simulator/rust_backend.py` | 新增 optional ctypes binding 和 `RustBackend.cross_detector_step` / `RustBackend.above_detector_step` |
| Tests | `EVAS/tests/test_rust_backend.py` | 用现有 Python detector 做 oracle，验证 Rust ABI 状态更新、触发方向、crossing time、debounce 和 above 初始触发语义 |
| Manifest | `behavior-coverage-map.v1.json` | B09 从 `python_only` 更新为 `partial` |

## Semantics Covered

`cross()` primitive 覆盖：

- uninitialized detector 初始化不触发；
- rising / falling / both direction 检测；
- exact touch 到零点时可触发但标记 `went_beyond = false`；
- linear interpolation 得到 crossing time；
- `last_cross_time` + `time_tol` debounce；
- crossing 后按 Python detector 语义夹到 post-crossing side，避免立即重复触发。

`above()` primitive 覆盖：

- 初次初始化时，如果已经 above，按 Python detector 立即触发；
- 从负侧穿越到 `>= -1e-12` 时触发；
- crossing time 线性插值；
- 触发后把 `prev_val` clamp 到 `>= 0`，保持 Python detector 的去重语义。

## What Is Still Python-Owned

| Remaining piece | Why not moved in 052 |
|---|---|
| event body execution | event body 可以任意写 state/output/timer/transition，必须和 generated Python evaluate 生命周期统一迁移 |
| event ordering | 多个 cross 在同一步内要按 crossing time 执行，当前 `_check_cross()` 还有 retrograde suppression 逻辑 |
| event interpolation context | `_event_time`、`_event_interpolated_nodes`、`_event_node_cross_directions` 会影响 event body 内的 `V(node)` 读值 |
| production engine wiring | 需要 B10 event body batch 和 B18 lifecycle executor 后才能安全默认启用 |

## Verification

Fresh checks:

```text
cargo test
23 passed

cargo build --release
passed

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_rust_backend.py -q
16 passed
```

`cargo fmt --check` is still not run because `rustfmt` is unavailable in the current local toolchain.

## Claim Boundary

This is a B09 primitive parity improvement, not a speed claim. It does not prove EVAS is faster than Spectre AX, and it does not mean the full Python EVAS event path has been Rustified.

The next safe step is either:

- B15 record/snapshot no-schema-change array primitive; or
- B17 simple dynamic bus descriptor/base+offset primitive; or
- B10/B18 shadow-only event trace after B09/B11 primitives are combined.
