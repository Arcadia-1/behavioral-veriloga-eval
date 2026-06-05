# 094g - Event Body Program Lowering

Status: `partial` (event trigger expression eval + Rust body write-set program; no due/order scheduler)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094c-schedule-ir.md`
- `094e-rust-abi.md`
- `094f-body-ir-encoder.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `EventBodyProgram` / `encode_event_body_program()`，把单个 `EventStatementIR` 的 trigger metadata 与 094f 的 Rust body write-set program 绑定起来；同时新增 standalone `evas_rust_evaluate_body_expr` ABI，让 future scheduler 可以单独计算 trigger expression 数值。现在可以表示“event scheduler 先计算 trigger expression 并判定事件触发，再让 Rust batch 执行该 event body 的 ordered writes”。该 audit 仍不实现 Rust event due/order scheduler，不接生产 dispatch，速度收益为 **0%**。

## Why This Exists

094f 已经能把普通 ordered write-set 编码成 Rust body ops，但 event-driven Verilog-A 的关键热路径通常是：

```verilog
@(cross(V(clk) - 0.5, +1)) begin
    q = q + 1;
    V(out) <+ q;
end
```

要把这类行为迁到 Rust，必须拆成两层：

```text
event due/order layer:
    cross(V(clk)-0.5,+1) 是否在当前 step 触发？
    如果多个 event 同时触发，源码顺序如何？

event body write-set layer:
    q = q + 1
    V(out) <+ q
```

本 audit 完成第二层和 trigger metadata 的绑定：`EventIR + BodyStmtProgram`。同时补了 standalone expression eval ABI，后续 scheduler 不需要伪造 write statement 就能计算 `cross(V(clk)-0.5,+1)` 里的 scalar expression value。

## What Changed

EVAS:

| File | Change |
|---|---|
| `evas/simulator/stmt_ir.py` | 新增 `EventBodyProgram` |
| `evas/simulator/stmt_ir.py` | 新增 `encode_event_body_program()` |
| `evas/rust_core/src/lib.rs` | 新增 `evaluate_body_expr_ops()` / `evas_rust_evaluate_body_expr()` |
| `evas/simulator/rust_backend.py` | 新增 `RustBackend.evaluate_body_expr()` |
| `tests/test_rust_backend.py` | 增加 standalone body expression eval bridge test |
| `tests/test_audit_094f_body_ir_encoder.py` | 增加 event body write-set positive/fallback tests，以及 trigger expression eval test |

Supported subset:

| Behavior | Status |
|---|---|
| Single `EventStatementIR` | supported |
| Event metadata retention | supported via existing `EventIR` |
| Event body scalar state assignment | supported through 094f body write-set encoder |
| Event body single-node voltage contribution | supported through 094f body write-set encoder |
| Ordered body execution | supported by Rust body ABI statement order |
| Standalone trigger expression value | supported through `evas_rust_evaluate_body_expr` |

Conservative fallback subset:

| Behavior | Reason |
|---|---|
| Event due/order computation | scheduler not implemented in this audit |
| `if/else` event body | branch phase-order and write-set selection need a separate gate |
| loop/case/system task event body | control-flow/stateful side effects not represented by the current body op ABI |
| dynamic indexed state/bus writes | flattened array/bus ownership not in this ABI |
| transition output inside event body | transition state/output scheduling is a separate runtime owner |

## Validation

```bash
cargo test --manifest-path EVAS/evas/rust_core/Cargo.toml --release
# 35 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094f_body_ir_encoder.py -q
# 7 passed

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_audit_094a_expr_ir.py \
  EVAS/tests/test_audit_094b_stmt_schedule_ir.py \
  EVAS/tests/test_audit_094d_state_binding_ir.py \
  EVAS/tests/test_audit_094f_body_ir_encoder.py \
  EVAS/tests/test_rust_backend.py -q
# 56 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests -q
# 628 passed
```

Tested event body:

```verilog
@(cross(V(clk) - 0.5, +1)) begin
    q = q + 1;
    V(out) <+ q;
end
```

Manual Rust body execution result after the due layer is assumed to have fired:

| Initial state | Expected | Rust result |
|---|---:|---:|
| `q=2.0`, `out=0.0` | `q=3.0`, `out=3.0` | `q=3.0`, `out=3.0` |

Tested trigger expression:

```verilog
cross(V(clk) - 0.5, +1)
```

Standalone Rust expression result:

| Input | Expected expression value | Rust result |
|---|---:|---:|
| `clk=0.7` | `0.2` | `0.2` |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| Engine dispatch changed? | no |
| Event due/order changed? | no |
| Cross/timer detector state changed? | no |
| CSV/checker changed? | no |
| Speed claim enabled? | no |

## Claim Boundary

**可以说**：

- 094g partial 已经能把一个 event trigger 与 Rust-executable body write-set 绑定成 program。
- 094g partial 已经能用 standalone Rust expression ABI 计算简单 trigger expression value。
- event body 的 ordered scalar state/output writes 可以通过 094e Rust ABI 执行。
- 对包含 control-flow 的 event body 仍保守 fallback。
- 全量 EVAS pytest 通过，说明默认生产路径未被破坏。

**不能说**：

- Rust event scheduler 已完成。
- cross/timer/above due/order 已经统一迁到 Rust。
- generic executor 可以 default-on。
- 当前改动带来速度提升。
- 当前改动已经证明 real-row waveform parity。

## Next Step

继续 094g：

1. 为 `EventIR` 增加 due/order scheduler ABI plan，先覆盖 `initial_step`、periodic `timer()`、simple `cross()`。
2. 将 scheduler 输出的 fired event index 与 `EventBodyProgram` 对接。
3. 做 shadow parity：同一步内 Python event order 与 Rust scheduler order 必须一致。
4. 再做 real-row waveform parity，之后才考虑 opt-in production dispatch。
