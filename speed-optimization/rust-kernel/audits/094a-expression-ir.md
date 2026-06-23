# 094a - Verilog-A Expression IR Foundation

Status: `done` (IR foundation only; no production runtime change)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `094-verilog-a-body-rust-kernel-design.md`
- `STAGE_2_4_EXECUTION_PLAN.md`
- `091-generic-event-state-transition-candidate-matcher.md`
- `091d-generic-executor-python-body.md`
- `095-generic-executor-record-adaptive-substeps.md`

## One-Line Summary

新增 `evas/simulator/expr_ir.py`，把 Verilog-A parser AST expression lowering 成通用 typed expression IR，并能 emit 回可编译 Python expression 做 round-trip 验证；release vabench 的 **234 个 `generic_event_state_transition_v1` candidate** 的 analog body 表达式根节点 **8156/8156 lower + emit compile 通过**。本 audit 不改变默认 backend，不接管 `model.evaluate()`，速度收益为 **0%**，价值是给后续 statement/event/Rust executor 建立通用表达式数据结构。

## Why This Exists

091d 已证明绕过 engine orchestration 能带来明显 wall reduction，但它仍在每个时间点调用 generated Python `model.evaluate()`。094 项目的目标是把 `evaluate()` body 本身 lower 到 Rust kernel。

要做这件事不能继续补小 helper。必须先把 Python AST 中的表达式统一表示成可以：

- 被 statement/event IR 引用；
- 被 Python emitter round-trip 验证；
- 后续编码成 Rust typed-array op；
- 在 unsupported function 或 side effect 出现时安全 fallback。

094a 只完成第一层：表达式 IR。

## What Changed

| Layer | Before | After |
|---|---|---|
| Expression IR | 只有 `evaluate_ir.py` 的 static-linear 小语言 | 新增 `expr_ir.py`，保留完整表达式树结构 |
| Lowering policy | scattered in backend helper methods | `LoweringContext` 明确 pure-math 和 Verilog-A body 两个口径 |
| Round-trip validation | 无通用 expression emitter | `emit_python(ir)` 可生成可编译 Python expression |
| Release coverage test | 无 094a gate | 新增 `test_audit_094a_expr_ir.py`，扫 234 个 091b generic candidate |

新增 IR 节点：

| IR node | 覆盖 Verilog-A AST |
|---|---|
| `LiteralIR` | number / string literal |
| `IdentifierIR` | scalar identifier, special identifiers are emitted as helper references |
| `ArrayAccessIR` | `arr[i]` |
| `BinaryExprIR` | `+ - * / %`, comparisons, bit ops, logical ops |
| `UnaryExprIR` | `- ! ~` |
| `TernaryExprIR` | `cond ? a : b` |
| `FunctionCallIR` | pure math, `transition`, `cross`, `last_crossing`, `$fopen`, random helpers under explicit body context |
| `BranchAccessIR` | `V(a)`, `V(a,b)`, dynamic-index branch access representation |
| `MethodCallIR` | currently `substr` representation |

## Important Boundary

`expr_ir.py` is broader than current Rust production semantics. It can represent expressions such as `transition(...)` and `$fopen(...)`, but later statement/event/Rust lowering must still decide whether those expressions are executable in Rust or require Python fallback.

This is intentional. 094a answers "can we preserve the expression tree without losing information?", not "can Rust execute every expression today?"

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094a_expr_ir.py -q
# 6 passed
```

Coverage from the release sweep test:

| Metric | Value |
|---|---:|
| Release `.va` files scanned | 357 |
| `generic_event_state_transition_v1` candidate models found | 234 |
| Candidate analog body expression roots checked | 8156 |
| Lowering failures | 0 |
| Python emit compile failures | 0 |

The test uses the same compiler metadata gate as 091b: a model counts only if `compile_module(parse(src))._whole_segment_candidates` includes `generic_event_state_transition_v1`.

## Speed Impact

| Metric | Value |
|---|---:|
| Default backend changed | no |
| Production Rust execution changed | no |
| EVAS wall speedup | 0% expected |

This audit is deliberately not a speed optimization by itself. It is the IR precondition for 094b-d statement/event/state lowering and 094e-g Rust executor work.

## Learning Note

可以把 094a 理解成给后续 Rust kernel 做"翻译词典"的第一章：

```text
Verilog-A source:
    V(out) <+ V(vdd, vss) * transition(q ? 1.0 : 0.0, 0, tr)

Parser AST:
    Contribution(BranchAccess("V", "out"), BinaryExpr("*", ...))

094a ExprIR:
    BinaryExprIR(
        "*",
        BranchAccessIR("V", "vdd", "vss"),
        FunctionCallIR("transition", ...)
    )
```

现在 IR 还没有执行；只是确保这棵树可以稳定、可测试地传给后续 statement/event lowering。

## Risks And Rollback

| Risk | Signal | Mitigation |
|---|---|---|
| IR 过宽导致后来误以为可 Rust production | 文档或后续代码把 representation 当 execution | 保留 `LoweringContext`，后续 production gate 必须重新检查 executable subset |
| Python emitter 语义不完全等价 generated backend | round-trip eval 出现行为差异 | 094a emitter 只用于 compile/smoke；真正 parity 在 094b-d/094e-g shadow 中验证 |
| Release candidate set 变化 | 234 candidate gate 失败 | 先检查 091b matcher 是否变化，再更新 audit claim |

Rollback: 删除 `expr_ir.py` 和 `test_audit_094a_expr_ir.py` 即可。没有 production hook。

## Claim Boundary

**可以说**：

- 094a 已建立通用 Verilog-A expression IR foundation。
- 234 个 091b generic candidate 的 analog body expression roots 全部可 lower 并 emit 成可编译 Python expression。
- 这一步没有改变默认仿真路径，功能风险低。

**不能说**：

- EVAS 已经把 `model.evaluate()` 全量 Rust 化。
- 094a 带来任何实际仿真速度提升。
- `transition/cross/timer/event body` 已由 Rust production 接管。
- 234 个 candidate 已具备 bit-exact Rust executor parity。

## Next Step

继续 094b/094c/094d：

1. `stmt_ir.py`：lower assignment / if / block / contribution / event body。
2. `schedule_ir.py`：lower cross/timer/initial_step schedule。
3. state/parameter binding：把 identifier/array/state/port 绑定到 typed slots。

进入 Rust ABI 前，必须先完成 Python round-trip parity，避免把不完整语义搬进 Rust 后再调试。
