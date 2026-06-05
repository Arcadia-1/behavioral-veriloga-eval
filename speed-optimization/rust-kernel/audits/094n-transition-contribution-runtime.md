# 094n - Transition Contribution Runtime

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/transition_runtime.py`
- `EVAS/tests/test_audit_094n_transition_runtime.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094m-event-only-runtime-builder.md`

## One-Line Summary

新增 094 transition contribution shadow runtime，把连续 `V(node[, ref]) <+ transition(...)` 输出桥接到已有 Rust transition-state primitive。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Continuous contribution coverage | 094 event-only runtime 不处理 `transition()` 输出 | 新增 `RustTransitionContributionRuntime` 处理 direct `transition()` voltage contribution | unchanged |
| Transition target evaluation | 依赖旧 static-linear transition target IR 或 Python `_transition()` | 用 094 BodyExpr batch 计算 target/delay/rise/fall，再调用 Rust `transition_state_step()` | unchanged |
| Transition breakpoint visibility | Rust runtime 内部知道 active ramp，但 engine 无法直接查询 | runtime 暴露 `next_breakpoint(time, min_ramp_time)`，供后续 engine contract 使用 | unchanged |
| Real benchmark coverage | `pipeline_stage` 只验证事件状态更新 | `pipeline_stage` 的 VRES/D1/D0 三个 transition 输出已由 Rust runtime 验证 | unchanged |

## Principle

这一步复用已有 Rust transition 数值内核，不重新实现 transition 波形。

执行流程：

```text
continuous contribution
  V(out, ref) <+ transition(target, delay, rise, fall)
    -> 094 BodyExpr batch evaluates target/delay/rise/fall
    -> Rust transition_state_step updates transition state arrays
    -> node_values[out] = node_values[ref] + transition_output
```

这比只支持 static-linear target 更通用，因为 target 可以是 094 BodyExpr stack-machine 支持的任意纯表达式，包括状态、参数、节点电压、ternary 和纯数学函数。当前仍只接受 direct `transition(...)` 作为 contribution RHS；`scale * transition(...) + offset` 这类 affine wrapper 后续再扩展。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| New 094n transition runtime tests | n/a | 2 pass | `pipeline_stage` 三个 transition 输出能由 Rust state step 写回 node array，并能暴露 transition ramp breakpoint |
| 094h/094n/094o targeted pytest | n/a | 10 pass | event due、transition runtime、combined analog-block runtime 保持一致 |
| 094 full targeted pytest + Rust ABI | n/a | 68 pass | 新 breakpoint contract 没破坏已有 094 IR/ABI/runtime |
| `pipeline_stage` continuous outputs | Python-owned only | Rust shadow runtime covered for direct transition contributions | 覆盖面推进，不是生产提速 |
| Production wall speed | unchanged | unchanged | 仍未接 `engine.py` |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094n_transition_runtime.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py EVAS/tests/test_audit_094o_analog_block_runtime.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094a_expr_ir.py EVAS/tests/test_audit_094b_stmt_schedule_ir.py EVAS/tests/test_audit_094d_state_binding_ir.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py EVAS/tests/test_rust_backend.py -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/stmt_ir.py EVAS/evas/simulator/event_due_runtime.py EVAS/evas/simulator/transition_runtime.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py
git diff --check -- evas/simulator/event_due_runtime.py evas/simulator/stmt_ir.py evas/simulator/transition_runtime.py tests/test_audit_094f_body_ir_encoder.py tests/test_audit_094h_event_due_program.py tests/test_audit_094n_transition_runtime.py
```

Results:

```text
2 passed in 0.68s
10 passed in 1.91s
68 passed in 12.76s
py_compile: pass
git diff --check: pass
```

## Learning Notes

`transition()` 不是普通数学函数。它内部有记忆：上一次 target 是什么、什么时候开始变、当前是否还在 ramp。Rust 化时不能只算 `transition(target)` 的当前表达式值，而要维护一组 transition state arrays：

- current value
- target value
- start time
- start value
- delay/rise/fall
- active flag
- initialized flag

094n 做的事情就是把这些数组集中起来，让一批 transition contribution 共享一次 Rust kernel 调用。后续如果接入 `engine.py`，这会减少每个输出每步单独走 Python `_transition()` 的开销。

094q 进一步说明，transition state 还必须向调度器暴露 `next_breakpoint()`。否则 Rust 虽然能算出 ramp 输出，Python engine 却不知道需要在 ramp 的 25%/50%/75%/end 时间点插入记录点，完整仿真波形会错位。094n 现在把这个查询做成 runtime API，但还没有默认接入 engine。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 只支持 direct `transition(...)`，暂不支持 `scale * transition(...) + offset` | affine wrapper 测试返回 `None` | 后续扩展 wrapper lowering，不改当前 direct path |
| 仍由 Python 调用 Rust batch，FFI/array packing 可能抵消小模型收益 | E2E wall 不下降或下降很小 | 保持 shadow，不接 production |
| reference node 语义写错会导致差分 contribution 输出偏移 | `V(out, ref)` fixture 失败 | 回退 `transition_runtime.py` |

## Next Step

下一篇审计文档编号和预期主题：

- `094o - Combined Event And Transition Shadow Runtime`
