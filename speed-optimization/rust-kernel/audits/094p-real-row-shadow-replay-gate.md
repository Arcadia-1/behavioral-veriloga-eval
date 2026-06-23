# 094p - Real-Row Shadow Replay Gate

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/prototypes/audit_094p_pipeline_stage_shadow_sweep.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094o-combined-analog-block-shadow-runtime.md`

## One-Line Summary

用真实 `pipeline_stage` row 的参考时间/输入网格 replay 094o Rust shadow runtime，验证输出波形和当前 EVAS reference 在同一时间点高度一致。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Real-row validation | 094o 只在单元测试中手动步进几个时间点 | 新增 094p prototype，对完整 763-row reference grid replay Rust shadow runtime | unchanged |
| Parity evidence | 有局部 state/output assertions | 有完整 `vres/d1/d0` same-grid waveform comparison | unchanged |
| Speed evidence | 无 real-row shadow runtime wall | 有 shadow replay wall，但不作为 E2E speed claim | unchanged |

## Principle

094p 是一个隔离式 gate：先不让 Rust runtime 拥有 adaptive scheduler，而是把当前 EVAS 参考 CSV 里的 `time/phi1/phi2/vin` 当作输入时间表，喂给 Rust shadow runtime。

这样可以把问题拆开：

- 如果 094p 不匹配，说明 Rust event/body/transition 语义本身还有错。
- 如果 094p 匹配，说明核心 analog-block runtime 可信，下一步才值得做 full-sim wrapper 或 engine opt-in dispatch。

它避免把 source waveform、adaptive step、breakpoint queue、CSV writer 这些外层因素混进第一道 Rust semantic gate。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Reference EVAS rows | n/a | 763 | 使用真实 `tb_pipeline_stage_ref.scs` 输出网格 |
| Reference EVAS wall | n/a | 1.715087s | 包含完整 EVAS sim + CSV |
| Rust shadow replay wall | n/a | 0.083317s | 只 replay analog-block runtime，不含 adaptive scheduler/source/CSV |
| Fired event count | n/a | 31 | initial/PHI1/PHI2 events 在完整时间表上触发 |
| Max output abs diff | n/a | 4.8599966967488584e-08 | `vres/d1/d0` same-grid 高精度匹配 |
| Max output rel_1v diff | n/a | 4.8599966967488584e-08 | 通过 1e-6 gate |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_094p_pipeline_stage_shadow_sweep.py
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/prototypes/audit_094p_pipeline_stage_shadow_sweep.py EVAS/evas/simulator/analog_block_runtime.py EVAS/evas/simulator/transition_runtime.py EVAS/evas/simulator/event_due_runtime.py EVAS/evas/simulator/stmt_ir.py
git diff --check -- prototypes/audit_094p_pipeline_stage_shadow_sweep.py evas/simulator/analog_block_runtime.py evas/simulator/event_due_runtime.py evas/simulator/stmt_ir.py evas/simulator/transition_runtime.py tests/test_audit_094f_body_ir_encoder.py tests/test_audit_094h_event_due_program.py tests/test_audit_094n_transition_runtime.py tests/test_audit_094o_analog_block_runtime.py
```

Results:

```text
reference EVAS:
- ok: True
- wall_s: 1.715087
- rows: 763
- csv_size: 74041

rust shadow replay:
- wall_s: 0.083317
- rows: 763
- fired_event_count: 31
- final_state: {'vin_s': 0.18, 'vres_level': 0.36, 'd1_level': 0.0, 'd0_level': 0.0}

same-grid output comparison:
- row_count_equal: True
- max_signal_abs: 4.8599966967488584e-08
- max_signal_rel_1v: 4.8599966967488584e-08
- per_signal_max_abs:
  - vres: 4.6329996394867123e-08
  - d1: 4.702500083775263e-08
  - d0: 4.8599966967488584e-08
- close_le_1e_6: True

decision:
SHADOW_REPLAY_PASSED_BUT_DO_NOT_DIRECT_WIRE_ENGINE
```

## Learning Notes

这一步里的 wall time 不能直接拿来 claim EVAS 加速。原因是 reference EVAS wall 包括完整仿真流程：source 更新、adaptive step、breakpoint、模型 evaluate、record/CSV；Rust shadow replay 只是在已有时间网格上重放 analog block。

它的价值是证明：如果外层调度把正确的时间点和 source 值交给 Rust，Rust 对 `pipeline_stage` 的核心模型行为能输出几乎相同的波形。也就是说，094 的下一风险已经从“Rust 语义是否正确”转移到“如何安全接入 scheduler/engine 并保持 E2E parity”。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| replay 复用 reference time grid，不能证明 Rust 自己能选对 adaptive step | full-sim wrapper CSV parity 失败 | 不接 production，先做 094q opt-in wrapper |
| shadow wall 比 reference 小很多但口径不对称 | 被误用为 speed claim | 文档明确禁止把 replay wall 当 E2E speedup |
| 只覆盖 `pipeline_stage` | 其他 real rows builder 返回 `None` 或 parity fail | 扩展 094p 到多 row sweep |

## Next Step

下一篇审计文档编号和预期主题：

- `094q - Opt-In Full-Sim Rust Shadow Wrapper`
