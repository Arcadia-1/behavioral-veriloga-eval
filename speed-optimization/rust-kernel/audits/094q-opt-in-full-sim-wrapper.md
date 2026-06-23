# 094q - Opt-In Full-Sim Rust Shadow Wrapper

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/prototypes/audit_094q_pipeline_stage_fullsim_wrapper.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094p-real-row-shadow-replay-gate.md`

## One-Line Summary

新增 prototype-only full-sim wrapper，让 `pipeline_stage` 在真实 EVAS engine 中通过 094o Rust runtime 执行模型主体，并验证它只能 time-aligned close，尚不能接 production。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Full simulation coverage | 094p 复用 reference time/source grid replay | 094q 让 EVAS engine 自己走步，model body 由 Rust shadow runtime 执行 | unchanged |
| Transition breakpoint ownership | 初版 wrapper 不把 Rust transition state 暴露给 engine，ramp 中间点丢失 | wrapper 将 Rust transition arrays 镜像到 `model.transitions`，engine 可继续扫描 transition breakpoint | unchanged |
| Production dispatch | 无 | 仍无；只在 prototype 中 monkey-patch `compile_module` | unchanged |

## Principle

094q 是 094p 之后的下一道更严格 gate。

094p 问的是：给 Rust 正确时间点和输入，它能不能算对输出？

094q 问的是：如果让现有 EVAS engine 正常走步，Rust wrapper 能不能在完整仿真中保持接近波形？

第一次 094q 运行失败，最大 time-aligned 输出误差约 0.2999V。检查 11ns 附近波形后发现不是事件体错误，而是 transition ramp 中间采样点缺失。原因是 Rust runtime 把 transition state 放在自己的 typed arrays 里，但 engine 的 `next_breakpoint()` 只看 `model.transitions`。修复方式是在 prototype wrapper 每步后把 Rust transition state 镜像回 `model.transitions`。

## Before / After Evidence

| Metric | Before transition-state mirror | After transition-state mirror | Interpretation |
|---|---:|---:|---|
| Reference EVAS wall | 1.566327s | 1.452739s | run-to-run variation |
| Rust 094q wrapper wall | 4.969771s | 3.219042s | wrapper 仍明显更慢 |
| Reference rows | 763 | 763 | stable |
| Rust wrapper rows | 752 | 761 | transition breakpoint visibility improved |
| Time-aligned max signal abs | 0.29990991139661183 | 0.00010972991426716483 | transition sampling issue largely fixed |
| Rowwise close | false | false | accepted grid still differs |
| Time-aligned <=1% | false | true | semantic smoke passes after alignment |

Final 094q decision:

```text
FULLSIM_WRAPPER_TIME_ALIGNED_PASS_BUT_DO_NOT_DIRECT_WIRE
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_094q_pipeline_stage_fullsim_wrapper.py
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/prototypes/audit_094q_pipeline_stage_fullsim_wrapper.py EVAS/prototypes/audit_094p_pipeline_stage_shadow_sweep.py EVAS/evas/simulator/analog_block_runtime.py EVAS/evas/simulator/transition_runtime.py EVAS/evas/simulator/event_due_runtime.py EVAS/evas/simulator/stmt_ir.py
git diff --check -- prototypes/audit_094q_pipeline_stage_fullsim_wrapper.py prototypes/audit_094p_pipeline_stage_shadow_sweep.py evas/simulator/analog_block_runtime.py evas/simulator/event_due_runtime.py evas/simulator/stmt_ir.py evas/simulator/transition_runtime.py tests/test_audit_094f_body_ir_encoder.py tests/test_audit_094h_event_due_program.py tests/test_audit_094n_transition_runtime.py tests/test_audit_094o_analog_block_runtime.py
```

Results after transition-state mirror:

```text
python_adaptive:
- ok: True
- wall_s: 1.452739
- rows: 763
- csv_size: 74041

rust094q_wrapper:
- ok: True
- wall_s: 3.219042
- rows: 761
- csv_size: 73847
- wrapper_models: 1
- wrapper_steps: 26714
- wrapper_fired_events: 31

rowwise:
- max_signal_abs: 0.9
- close_le_1pct: False

time-aligned:
- max_nearest_time_delta: 1.2207030000818605e-13
- max_signal_abs_interp: 0.00010972991426716483
- max_signal_rel_1v_interp: 0.00010972991426716483
- close_le_1pct_interp: True

py_compile: pass
git diff --check: pass
```

## Learning Notes

这一步暴露了一个很关键的工程事实：Rust 化不能只把计算搬过去，还要把“仿真器调度需要看的状态”同步出来。

`transition()` 的状态不只是输出值，它还告诉 engine：

- 当前 ramp 是否 active；
- ramp 从什么时候开始；
- rise/fall 多久；
- 下一个需要插入的 breakpoint 是什么时候。

如果 Rust 内部维护了这些状态，但 Python engine 看不到，engine 就不会在 ramp 中间插入记录点，CSV 波形会少点或错位。094q 修复了 prototype 中的 transition visibility，但 rowwise grid 仍不一致，说明 engine dispatch 前还需要更完整的 phase/order/breakpoint gate。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| wrapper 每步 Python pack/sync 太重 | 094q wall 3.219s，比 Python adaptive 1.453s 慢 | 不接 production；后续必须做 persistent typed arrays / engine-native dispatch |
| time-aligned pass 被误当成 rowwise parity | rowwise max_signal_abs 仍 0.9 | production gate 必须要求 release-wide CSV policy，而不是只看单 row time-aligned smoke |
| transition state mirror 只是 prototype 层修复 | engine.py 真实接线还没有这套 ownership contract | 094r 先定义 engine dispatch contract |

## Next Step

下一篇审计文档编号和预期主题：

- `094r - Engine Dispatch Contract And No-Default Decision`
