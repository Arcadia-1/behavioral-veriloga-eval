# vaBench-main-v1 Main120 Validation Report

**Date**: 2026-05-08

This report records the first complete `vaBench-main-v1` build target:
30 concrete circuit-function packs x 4 task forms = 120 tasks.

## Benchmark Root

```text
benchmark-vabench-main-v1/
```

## Scale

| Split | Packs | Tasks | Status |
| --- | ---: | ---: | --- |
| `vaBench-dev48` | 12 | 48 | Existing development/smoke benchmark |
| `vaBench-main-v1` | 30 | 120 | Materialized and gold-validated here |
| `vaBench-heldout-v1` | 12 planned | 48 planned | Not materialized in this step |

## Current Main Packs

| Pack | Mechanism family |
| --- | --- |
| `offset_comparator` | threshold/static nonlinear |
| `strongarm_comparator_behavior` | threshold/static nonlinear |
| `voltage_clamp` | threshold/static nonlinear |
| `precision_rectifier` | threshold/static nonlinear |
| `peak_detector` | stateful analog memory |
| `track_hold_aperture` | stateful analog memory |
| `debounce_latch` | stateful analog memory |
| `leaky_hold` | stateful analog memory |
| `edge_detector` | event/timing |
| `one_shot_timer` | event/timing |
| `resettable_counter_divider` | event/timing |
| `pfd_reset_race` | event/timing |
| `thermometer_dac` | data conversion |
| `segmented_dac` | data conversion |
| `sar_logic_4b` | data conversion |
| `cdac_calibration` | data conversion/calibration |
| `offset_calibration_fsm` | calibration/control |
| `gain_trim_controller` | calibration/control |
| `lock_detector` | calibration/control |
| `background_calibration_accumulator` | calibration/control |
| `rotating_element_selector` | pointer/selection |
| `barrel_pointer_window` | pointer/selection |
| `element_shuffler` | pointer/selection |
| `thermometer_decoder_guarded` | pointer/selection |
| `first_order_lowpass` | continuous dynamics |
| `resettable_integrator` | continuous dynamics |
| `slew_rate_limiter` | continuous dynamics |
| `vco_phase_integrator` | continuous dynamics/pll |
| `settling_time_measurement_tb` | source/measurement/TB |
| `file_metric_writer` | source/measurement/TB |

## Audit Gates

| Gate | Scope | Result | Artifact |
| --- | --- | --- | --- |
| Semantic prompt/checker/gold audit | all 120 tasks | `120 PASS / 0 WARN / 0 FAIL` | `analysis/vabench-main-v1_semantic_contract_audit_20260508.json` |
| Benchmark integrity audit | all 120 tasks | `PASS`, no issues | `analysis/vabench-main-v1_integrity_audit_20260508.json` |
| Draft7 reuse hash audit | reused 28 tasks | `PASS`, current gold matches staged Draft7 gold | `analysis/vabench-main-v1_draft7_reuse_hash_audit_20260508.json` |
| Draft11 reuse hash audit | reused 16 tasks | `PASS`, current gold matches staged Draft11 gold | `analysis/vabench-main-v1_draft11_new4_reuse_hash_audit_20260508.json` |
| Full Main120 strict-EVAS | all 120 tasks | `120/120 PASS` | `results/vabench-main-v1-main120-gold-evas-2026-05-08/summary.json` |
| Full Main120 Spectre | all 120 tasks | `120/120 PASS` | `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/summary.json` |
| New19 strict-EVAS | new/changed 76 tasks | `76/76 PASS` | `results/vabench-main-v1-draft30-new19-gold-evas-2026-05-08/summary.json` |
| New19 Spectre | new/changed 76 tasks | `76/76 PASS` | `results/vabench-main-v1-draft30-new19-gold-spectre-jin-2026-05-08/summary.json` |
| Reused Draft7 strict-EVAS/Spectre | unchanged 28 tasks | `28/28`, `28/28` | `results/vabench-main-v1-draft7-gold-*/summary.json` |
| Reused Draft11 strict-EVAS/Spectre | unchanged 16 tasks | `16/16`, `16/16` | `results/vabench-main-v1-draft11-new4-gold-*/summary.json` |

Full-run gold evidence: `120/120` tasks pass strict-EVAS and `120/120` tasks pass Spectre in direct Main120 runs. Incremental composed evidence is retained as supporting/debug evidence.

## Confidence Loop Fixes

During the fill-to-120 pass, the following benchmark-side issues were caught and
fixed before promotion:

| Issue | Symptom | Fix |
| --- | --- | --- |
| Extra-pack prompts did not expose exact transient line | semantic audit gave `gold_tran_not_public` WARN for 76 new tasks | generated prompts now include exact `tran ... stop=... maxstep=...` line |
| Calibration/checker windows averaged across sign-change phases | first EVAS pass for new19 was `60/76`; failures were only calibration/control behavior checks | checkers now use fixed phase sample points for increase/decrease/increase behavior |

After these fixes, full semantic/integrity audits are clean and new19 EVAS/Spectre
both pass `76/76`.

## Commands

```bash
python3 runners/materialize_vabench_main_seed.py --output-bench benchmark-vabench-main-v1 --force
python3 runners/audit_bpack_semantic_contracts.py --bench-dir benchmark-vabench-main-v1 --output-dir analysis
python3 runners/audit_vabench_benchmark_integrity.py --bench-dir benchmark-vabench-main-v1 --output-dir analysis

python3 runners/audit_vabench_result_reuse.py \
  --bench-dir benchmark-vabench-main-v1 \
  --result-dir results/vabench-main-v1-draft7-gold-evas-2026-05-08 \
  --output analysis/vabench-main-v1_draft7_reuse_hash_audit_20260508.json
python3 runners/audit_vabench_result_reuse.py \
  --bench-dir benchmark-vabench-main-v1 \
  --result-dir results/vabench-main-v1-draft11-new4-gold-evas-2026-05-08 \
  --output analysis/vabench-main-v1_draft11_new4_reuse_hash_audit_20260508.json

python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft30-new19 \
  --backend evas \
  --task <new19 task ids> ... \
  --output-dir results/vabench-main-v1-draft30-new19-gold-evas-2026-05-08 \
  --timeout-s 180

python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft30-new19 \
  --backend spectre \
  --task <new19 task ids> ... \
  --output-dir results/vabench-main-v1-draft30-new19-gold-spectre-jin-2026-05-08 \
  --timeout-s 180 \
  --env /Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite/.env \
  --profile jin
```

## Promotion State

| Gate | Status |
| --- | --- |
| 30 concrete circuit-function packs | PASS |
| Four task forms per pack | PASS: 30/30 packs |
| Semantic prompt/checker/gold audit | PASS: 120/120 |
| Benchmark integrity audit | PASS |
| Gold strict-EVAS evidence | PASS: full run 120/120 |
| Gold Spectre evidence | PASS: full run 120/120 |
| Heldout split | TODO: planned 12 packs / 48 tasks |
| Model matrix A/D/C/S1/S2 | TODO after final review/freeze |

## Residual Risks

| Risk | Mitigation |
| --- | --- |
| Incremental result reuse still depends on staged gold hashes, not full rerun | Full 120-task EVAS/Spectre audit now exists; rerun only after benchmark, validator, EVAS kernel, or Spectre bridge changes |
| Some new packs are intentionally compact behavioral abstractions | Treat Main120 as first clean benchmark; heldout and v2 can add harder/noisier circuits |
| Skill/RAG/controller may overfit Main120 | Keep `vaBench-heldout-v1` separate and do not tune methods on heldout |
