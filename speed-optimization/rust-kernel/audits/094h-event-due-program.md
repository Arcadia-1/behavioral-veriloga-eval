# 094h - Event Due Program and Trigger Expression Batch

Status: `partial` (Rust trigger input batch; no fired-index/order scheduler)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094c-schedule-ir.md`
- `094e-rust-abi.md`
- `094f-body-ir-encoder.md`
- `094g-event-body-program.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `EventDueProgram` / `encode_event_due_program()`，把 `initial_step`、simple `cross()`、`above()`、static `timer()` trigger lower 成 typed-array / Rust expression segment；同时新增 `evas_rust_evaluate_body_expr_batch`，一次 FFI 调用可计算多个 trigger/timer expression value。该 audit 仍不负责 detector state、fired event ordering、event body production dispatch，因此速度收益仍记为 **0%**。

## Why This Exists

094g 证明了 event body 的 ordered write-set 可以由 Rust 执行，但还缺少 event scheduler 所需的输入：

```text
Verilog-A EventIR
  -> trigger expression segments
  -> node/state/parameter typed arrays
  -> detector/timer queue
  -> fired event indices in source order
  -> event body write-set execution
```

本 audit 完成前两步。这样后续不需要按端口名或 benchmark 名字匹配，而是通过 `BindingTableIR + node_slots` 把语义表达式映射为稳定 slot。

## What Changed

EVAS:

| File | Change |
|---|---|
| `evas/simulator/schedule_ir.py` | 新增 `EventDueTriggerProgram` / `EventDueProgram` |
| `evas/simulator/schedule_ir.py` | 新增 `encode_event_due_program()`、`event_due_expr_segments()`、`event_due_timer_segments()` |
| `evas/rust_core/src/lib.rs` | 新增 `evaluate_body_expr_segments()` / `evas_rust_evaluate_body_expr_batch()` |
| `evas/simulator/rust_backend.py` | 新增 `RustBodyExprBatch`、`RustBackend.evaluate_body_expr_batch()` |
| `tests/test_rust_backend.py` | 增加 expression-segment batch ABI test |
| `tests/test_audit_094h_event_due_program.py` | 增加 combined cross/above/static timer due-program lowering tests |

Supported trigger subset:

| Trigger | Status |
|---|---|
| `initial_step` | encoded as an ordered trigger marker |
| `cross(expr, dir, ttol, vtol)` | trigger expression encoded to Rust body expression ops; direction/tolerances preserved |
| `above(expr)` | trigger expression encoded to Rust body expression ops |
| `timer(start)` | encoded only when `start` is static parameter/literal expression |
| `timer(start, period)` | encoded only when both expressions are static parameter/literal expressions |

Conservative fallback:

| Behavior | Reason |
|---|---|
| dynamic timer expression reading node/state | timer target ownership and re-arm semantics need a separate state-owned queue gate |
| `final_step` | not part of hot event due path yet |
| detector state mutation | existing Rust primitive exists, but this audit only prepares trigger values |
| fired event ordering | not implemented in this audit |
| production dispatch | not changed |

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_rust_backend.py \
  EVAS/tests/test_audit_094f_body_ir_encoder.py \
  EVAS/tests/test_audit_094h_event_due_program.py -q
# 48 passed

cargo test --manifest-path EVAS/evas/rust_core/Cargo.toml --release
# 36 passed
```

Tested source pattern:

```verilog
@(initial_step or cross(V(clk) - vth, +1, 1p, vtol) or above(V(inp) - 0.2))
    q = q + 1;
```

Rust batch trigger values:

| Inputs | Expected | Rust batch |
|---|---:|---:|
| `clk=0.75`, `vth=0.5` | `0.25` | `0.25` |
| `inp=0.1` | `-0.1` | `-0.1` |

Tested static timer:

```verilog
@(timer(t0, per)) q = q + 1;
```

Rust batch timer expression values:

| Parameter | Expected | Rust batch |
|---|---:|---:|
| `t0` | `1e-9` | `1e-9` |
| `per` | `2e-9` | `2e-9` |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| Engine dispatch changed? | no |
| Detector/timer state changed? | no |
| Event body production changed? | no |
| CSV/checker changed? | no |
| Speed claim enabled? | no |

## Claim Boundary

**可以说**：

- 094h 可以把 supported `EventIR` trigger 编成 Rust expression batch input。
- 094h 的 trigger lowering 是语义/slot 驱动，不依赖 benchmark 名或固定端口名。
- 多个 trigger/timer expression 可以一次 FFI 调用由 Rust 求值。

**不能说**：

- Rust event scheduler 已完成。
- cross/above/timer detector state 和 fired-order 已由 Rust 统一接管。
- event body 已经按 fired order 自动生产执行。
- 当前改动带来真实速度提升。
- 当前改动已经证明 real-row waveform parity。

## Next Step

继续 094i：

1. 把 `EventDueProgram` 的 trigger values 接到已有 Rust `cross_detector_step` / `above_detector_step` / timer primitives。
2. 输出 fired event index list，并保持源码顺序。
3. 将 fired index 与 `EventBodyProgram` body write-set batch 连接，先做 shadow parity。
4. 只有 real-row waveform parity 通过后，才考虑 opt-in production dispatch。
