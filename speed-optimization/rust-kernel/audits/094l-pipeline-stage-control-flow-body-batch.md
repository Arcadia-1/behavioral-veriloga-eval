# 094l - Pipeline Stage Control-Flow Body Batch

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/prototypes/audit_094l_pipeline_stage_roundtrip.py`
- `EVAS/tests/test_audit_094f_body_ir_encoder.py`

## One-Line Summary

把 094 从 helper-based smoke 推进一步：真实 `pipeline_stage` 的 PHI2 事件体中 `if/else + clamp` 写集现在可以编码并由 Rust body batch 执行。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Statement encoder | `IfStatementIR` 事件体被 body encoder 拒绝 | 支持保守 `if/else` 子集，把分支写集 lowering 成表达式级 `SELECT` | unchanged |
| Real benchmark coverage | `pipeline_stage` 只能通过 helper round-trip smoke 说明波形接近 | PHI2 事件体的上/中/下区间和上下 clamp 已直接由 Rust body batch 验证 | unchanged |
| Production dispatch | `engine.py` 不调用 094 Rust body batch | 仍不调用，等待 scheduler/phase-order/typed-array dispatch gate | unchanged |

## Principle

这一步本身不是直接加速，而是移除后续加速的语义缺口。

核心思想是：Verilog-A 里的

```verilog
if (cond) x = a;
else x = b;
```

可以先表示成表达式：

```text
x = cond ? a : b
```

然后交给已有 Rust stack-machine 执行。这样 Rust 不需要先实现完整 Python 式语句解释器，就能覆盖大量事件体里的条件赋值。

为了避免错误改变语义，这次只接受保守子集：

- then/else 两边必须写同一组 target，顺序一致；
- 无 else 的 clamp 形式会变成 `cond ? new_value : old_value`；
- 多写 target 且条件读取被本分支改写的 state 时拒绝，避免第二个写入看到已变化的条件。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| 094f/094h targeted pytest | 12 pass / 1 fail after encoder change | 14 pass | 测试口径已从“拒绝控制流”升级为“Rust 执行控制流” |
| `pipeline_stage` PHI2 body Rust batch | not directly tested | pass | 真实 top-row 事件体可由 Rust body batch 执行 |
| `pipeline_stage` round-trip wall | Python adaptive 1.014684s | emit094 helper 1.561915s | 094 helper prototype 仍慢，不能接 production |
| Time-aligned waveform diff | n/a | max abs 1.0973e-4, within 1% | helper round-trip parity smoke 通过 |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/stmt_ir.py EVAS/tests/test_audit_094f_body_ir_encoder.py
git diff --check -- evas/simulator/stmt_ir.py tests/test_audit_094f_body_ir_encoder.py
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_094l_pipeline_stage_roundtrip.py
```

Results:

```text
14 passed in 0.85s
py_compile: pass
git diff --check: pass

pipeline_stage round-trip:
- Python adaptive wall: 1.014684s
- emit094 helper wall: 1.561915s
- rowwise comparison is not close because accepted time grids differ
- time-aligned max_signal_abs_interp: 0.00010972991426716483
- decision: PARITY_SMOKE_PASSED_BUT_DO_NOT_DIRECT_WIRE_ENGINE
```

## Learning Notes

`if/else` Rust 化有两种路线：

1. 在 Rust 里实现完整语句解释器，像 Python 一样逐句执行。
2. 把简单条件赋值改写成表达式选择：`cond ? true_value : false_value`。

这次走的是第 2 条，因为它复用已有 Rust expression stack-machine，改动小、可测试、风险低。它能覆盖 `pipeline_stage` 这类常见“事件触发后根据阈值写状态”的行为，但还不是完整 Verilog-A 控制流。

为什么暂时没有速度提升：完整仿真仍然没有从 `engine.py` 调用这个 Rust batch。现在只是证明“这段行为可以 Rust 化且结果正确”。真正提速还需要把 event due、event body、transition output、record/CSV 放进同一个 typed-array 路径里，避免 Python 在每一步继续打包/同步 dict。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 条件表达式在 Rust stack-machine 中 eager evaluation，极端情况下可能提前计算未执行分支 | 含除零或副作用表达式的新测试失败 | 回退 `stmt_ir.py` 的 `IfStatementIR` encoder 子集 |
| 多 target 写入的条件依赖被改写 state，可能改变后续 target 的条件判断 | encoder 应返回 `None`；若误接受，新增 regression 会失败 | 收紧 `_collect_conditional_write_specs` |
| 误以为 094 已经 production-ready | round-trip smoke 显示 helper 仍慢，且 `engine.py` 未接线 | 保持 091d 为生产推荐路径 |

## Next Step

下一篇审计文档编号和预期主题：

- `094m - Event Body Scheduler Dispatch Gate`
