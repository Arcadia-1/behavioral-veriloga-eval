# 094c - Event Schedule IR Foundation

Status: `done` (IR foundation only; no event queue production change)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `094a-expression-ir.md`
- `094b-statement-ir.md`
- `094-verilog-a-body-rust-kernel-design.md`
- `095-generic-executor-record-adaptive-substeps.md`

## One-Line Summary

新增 `evas/simulator/schedule_ir.py`，把 Verilog-A event control lowering 成 event schedule IR，覆盖 `cross/timer/initial_step/final_step/combined event` 的结构表示。该 IR 被 094b statement IR 引用；release 234 个 generic candidate 的 event statements 全部可 lower + emit compile。默认 event queue/order/interpolation 仍由 Python 拥有。

## What Changed

新增 event schedule IR：

| IR node | 覆盖事件 |
|---|---|
| `EventTriggerIR` | 单个 `EventExpr`，包括 `event_type`、args、direction、time/expr tolerance |
| `CombinedEventIR` | `event1 or event2` |

`lower_event()` 使用 094a expression IR lowering event args，比如：

```text
@(cross(V(clk) - 0.45, +1))
=> EventTriggerIR(
     event_type="CROSS",
     args=(BinaryExprIR("-", BranchAccessIR("V", "clk"), LiteralIR(0.45)),),
     direction=+1
   )
```

## Why This Matters

091d/095 的 parity gap 主要来自 event-time/adaptive schedule 差异，而不是单个 `transition()` 计算。后续 Rust executor 如果要 default-on，必须拥有完整 event schedule 表示：

- event due 检测；
- event ordering；
- interpolated cross time；
- event body dispatch；
- post-event output/record timing。

094c 只建立表示层，不尝试接管这些语义。

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094b_stmt_schedule_ir.py -q
# 4 passed
```

The release sweep is shared with 094b:

| Metric | Value |
|---|---:|
| `generic_event_state_transition_v1` candidate models | 234 |
| Statement/schedule lowering failures | 0 |
| Python body emit compile failures | 0 |

Observed event mix in the 234 candidates during pre-implementation audit:

| Event type | Count |
|---|---:|
| `INITIAL_STEP` | 234 |
| `CROSS` | 272 |
| `TIMER` | 61 |
| `FINAL_STEP` | 2 |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| Event queue/order changed? | no |
| Cross interpolation changed? | no |
| Timer state changed? | no |
| CSV trace changed? | no |

## Claim Boundary

**可以说**：

- 094c 已经把 234 个 generic candidate 的 event controls 表示成 schedule IR。
- `cross/timer/initial/final/combined` 的 event structure 可以被后续 Rust executor 消费。

**不能说**：

- Rust 已经接管 event queue。
- `cross()` interpolation parity 已经解决。
- `timer()` state/order 已经全量 Rust 化。
- 091d/095 的 CSV parity outlier 已经被修复。

## Next Step

094d state/parameter binding 必须把 event schedule 和 statement IR 中的 identifier 绑定到 typed slots。之后才有条件进入 094e Rust ABI。
