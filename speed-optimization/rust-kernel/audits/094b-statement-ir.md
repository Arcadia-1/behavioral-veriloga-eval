# 094b - Verilog-A Statement IR Foundation

Status: `done` (IR foundation only; no production runtime change)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `094a-expression-ir.md`
- `094c-schedule-ir.md`
- `094-verilog-a-body-rust-kernel-design.md`
- `STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `evas/simulator/stmt_ir.py`，把 Verilog-A analog block statement lowering 成 typed statement IR；release vabench 的 **234 个 `generic_event_state_transition_v1` candidate** analog block 全部 lower 成 statement IR，并 emit 成可编译 Python function body。该 audit 仍不改变 simulator production path，速度收益为 **0%**。

## What Changed

新增 statement IR 节点：

| IR node | 覆盖语句 |
|---|---|
| `AssignmentIR` | scalar / array assignment target |
| `ContributionIR` | `V(...) <+ expr` contribution |
| `EventStatementIR` | `@(event) body` |
| `BlockIR` | `begin ... end` |
| `IfStatementIR` | `if/else` |
| `ForStatementIR` | `for` representation |
| `WhileStatementIR` | `while` representation |
| `CaseStatementIR` | `case/default` representation |
| `SystemTaskIR` | `$bound_step/$fwrite/$fclose/...` representation under explicit policy |

The new `StatementLoweringContext` uses 094a's `LoweringContext.veriloga_body()` for expression lowering and keeps system tasks behind an explicit allowed list.

## Why This Works

094a already proved the expression tree can be preserved. 094b lifts one level up:

```text
expression IR:   q ? 1.0 : 0.0
statement IR:    V(out) <+ V(vdd, vss) * transition(q ? 1.0 : 0.0, ...)
event body IR:   if (q == 0) q = 1; else q = 0;
```

This still does not execute Rust. It only gives the future executor a structured body instead of relying on generated Python source text.

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094b_stmt_schedule_ir.py -q
# 4 passed
```

Release sweep inside the test:

| Metric | Value |
|---|---:|
| `generic_event_state_transition_v1` candidate models | 234 |
| Statement lowering failures | 0 |
| Python body emit compile failures | 0 |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| `model.evaluate()` production path changed? | no |
| CSV schema changed? | no |
| Event ordering changed? | no |
| System task behavior changed? | no |

## Claim Boundary

**可以说**：

- 094b 已经能把 234 个 091b generic candidate 的 analog block 表示成 statement IR。
- Statement IR emit 可以生成可编译 Python body，用于后续 round-trip validation。

**不能说**：

- statement IR 已经具备 bit-exact runtime parity。
- event body 已由 Rust production 执行。
- `$bound_step/$fwrite/$fclose` 已有 Rust 语义；当前只是 representation。
- EVAS 有任何新速度提升。

## Next Step

094d 需要做 state/parameter binding：把 `IdentifierIR("q")` 这类名字绑定到 typed state/param/node slot。没有 binding，Rust executor 仍无法避免 Python dict/string lookup。
