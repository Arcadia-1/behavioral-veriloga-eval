# 094m - Event-Only Runtime Builder

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/event_due_runtime.py`
- `EVAS/tests/test_audit_094h_event_due_program.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094l-pipeline-stage-control-flow-body-batch.md`

## One-Line Summary

新增一个保守的 event-only Rust runtime 构建器，把真实模型里的多个事件语句按 source order 连接到 094 due/body Rust batch。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Runtime construction | 测试里手动为每个 event statement 拼 `RustEventStatementRuntime` | 新增 `try_build_rust_event_only_analog_block_runtime()` 自动扫描 analog block 事件语句 | unchanged |
| Fallback gate | 单个 due/body encoder 失败只能由调用方零散处理 | 只要任一事件不能编码，构建器整体返回 `None` | unchanged |
| Real benchmark sequence | `pipeline_stage` PHI2 body 单独验证 | `initial_step -> PHI1 cross -> PHI2 cross` 三个事件由同一个 event-only runtime 执行 | unchanged |

## Principle

这一步解决的是“连接问题”，不是直接解决最终速度。

094l 已经证明 PHI2 的复杂事件体可以 Rust 化；094m 把多个事件语句按源码顺序串起来。这样后续接 `engine.py` 时不需要为每个 benchmark 手写事件 runtime，而是走同一个构建入口：

```text
module analog block
  -> lower_stmt(event statement)
  -> encode_event_due_program()
  -> encode_event_body_program()
  -> RustEventStatementRuntime
  -> RustAnalogBlockEventRuntime
```

如果任一步失败，返回 `None`，生产路径必须 fallback 到现有 Python/091d。这个 gate 很重要：Rust 化不能靠特例硬接，必须能自动拒绝尚未支持的语义。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| 094f/094h targeted pytest | 14 pass after 094l | 15 pass | 新增真实 `pipeline_stage` event-only runtime sequence 测试 |
| 094 full targeted pytest + Rust ABI | 64 pass after 094l | 65 pass | 094m 没破坏已有 IR/ABI/runtime 测试 |
| `pipeline_stage` event sequence | manual/not covered | pass | 初始事件、PHI1 采样、PHI2 条件计算能串起来 |
| Production wall speed | unchanged | unchanged | 仍未接 `engine.py`，不声明提速 |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094f_body_ir_encoder.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094a_expr_ir.py EVAS/tests/test_audit_094b_stmt_schedule_ir.py EVAS/tests/test_audit_094d_state_binding_ir.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_rust_backend.py -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/stmt_ir.py EVAS/evas/simulator/event_due_runtime.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py
git diff --check -- evas/simulator/event_due_runtime.py evas/simulator/stmt_ir.py tests/test_audit_094f_body_ir_encoder.py tests/test_audit_094h_event_due_program.py
```

Results:

```text
15 passed in 1.17s
65 passed in 28.08s
py_compile: pass
git diff --check: pass
```

## Learning Notes

这一步里的 “event-only” 是一个刻意限制。

Verilog-A analog block 里通常混有两类语句：

- `@(cross(...)) begin ... end`：事件到了才执行，用来更新状态。
- `V(out) <+ transition(state, ...)`：连续输出，每个仿真步都要根据当前状态更新波形。

094m 只处理第一类事件语句。它能让 Rust 接管“什么时候事件触发、触发后状态怎么改”，但还没有接管连续输出、transition breakpoint、record/CSV。所以它是通往生产 Rust kernel 的中间层，不是最终仿真器。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 开发者误把 event-only runtime 当成完整 analog block runtime | transition/continuous contribution 没有输出变化 | 保持函数名含 `event_only`，并在 docstring 中声明限制 |
| 某个真实模型事件语句无法编码 | 构建器返回 `None` | fallback 到 Python/091d |
| 事件 source order 被破坏 | source-order runtime 测试失败 | 回退 `try_build_rust_event_only_analog_block_runtime()` |

## Next Step

下一篇审计文档编号和预期主题：

- `094n - Continuous Contribution And Transition Dispatch Gate`
