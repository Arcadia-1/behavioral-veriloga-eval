# vaBench-main-v1 Draft11 Validation Report

**Date**: 2026-05-08

This report records the current audited benchmark expansion state for
`vaBench-main-v1`: 11 circuit-function packs x 4 task forms = 44 tasks.
Draft11 extends Draft7 with four additional packs and validates only the new or
changed simulator targets with EVAS/Spectre while reusing unchanged Draft7
simulator evidence.

## Benchmark Root

```text
benchmark-vabench-main-v1/
```

## Current Packs

| Pack | Forms | Mechanism family | Draft status |
| --- | ---: | --- | --- |
| `offset_comparator` | 4 | threshold/static nonlinear | Draft7 PASS, reused |
| `strongarm_comparator_behavior` | 4 | threshold/static nonlinear | Draft7 PASS, reused |
| `voltage_clamp` | 4 | threshold/static nonlinear | Draft7 PASS, reused |
| `pfd_reset_race` | 4 | event/timing | Draft7 PASS, reused |
| `resettable_counter_divider` | 4 | event/timing | Draft7 PASS, reused |
| `track_hold_aperture` | 4 | stateful analog memory | Draft7 PASS, reused |
| `sar_logic_4b` | 4 | data conversion | Draft7 PASS, reused |
| `one_shot_timer` | 4 | event/timing | Draft11 new PASS |
| `thermometer_dac` | 4 | data conversion | Draft11 new PASS |
| `lock_detector` | 4 | calibration/control | Draft11 new PASS |
| `resettable_integrator` | 4 | continuous dynamics | Draft11 new PASS |

## Audit Gates

| Gate | Scope | Result | Artifact |
| --- | --- | --- | --- |
| Semantic prompt/checker/gold audit | all 44 tasks | `44 PASS / 0 WARN / 0 FAIL` | `analysis/vabench-main-v1_semantic_contract_audit_20260508.json` |
| Benchmark integrity audit | all 44 tasks | `PASS`, no issues | `analysis/vabench-main-v1_integrity_audit_20260508.json` |
| Gold strict-EVAS | new/changed 16 tasks | `16/16 PASS` | `results/vabench-main-v1-draft11-new4-gold-evas-2026-05-08/summary.json` |
| Gold Spectre | new/changed 16 tasks | `16/16 PASS` | `results/vabench-main-v1-draft11-new4-gold-spectre-jin-2026-05-08/summary.json` |
| Reused Draft7 strict-EVAS | unchanged 28 tasks | `28/28 PASS` | `results/vabench-main-v1-draft7-gold-evas-2026-05-08/summary.json` |
| Reused Draft7 Spectre | unchanged 28 tasks | `28/28 PASS` | `results/vabench-main-v1-draft7-gold-spectre-jin-2026-05-08/summary.json` |
| Draft7 reuse hash audit | unchanged 28 tasks | `PASS`, current gold matches staged Draft7 gold | `analysis/vabench-main-v1_draft7_reuse_hash_audit_20260508.json` |

Composed evidence: `44/44` gold tasks have strict-EVAS and Spectre pass evidence
under unchanged-task reuse plus new-task incremental validation.

## Confidence Loop Fixes

The first incremental EVAS pass found benchmark-side issues before promotion:

| Issue | Location | Symptom | Fix |
| --- | --- | --- | --- |
| Too-small integrator gain | `resettable_integrator` gold DUT | likely semantic under-drive against checker thresholds | changed default `gain` from `1.0e6` to `1.0e9` |
| DAC PWL samples on ramps | `thermometer_dac` gold TB | EVAS checker saw unstable public input codes, `12/16` new-task EVAS pass | moved code transitions between checker sample points |

After these fixes, full semantic and integrity audits remained clean, and the
new 16-task EVAS/Spectre gates both passed.

## Incremental Validation Policy Used

Default expansion policy:

1. Run full semantic prompt/checker/gold audit on all benchmark tasks.
2. Run full benchmark integrity audit on all benchmark tasks.
3. Run EVAS and Spectre only for new or changed tasks.
4. Reuse prior EVAS/Spectre results for unchanged tasks.
5. Trigger full EVAS/Spectre rerun only when old task prompt/gold/checker files
   changed, validator/preflight/kernel behavior changed, or the benchmark is
   being frozen for a release/paper table.

This avoids wasting time on unchanged gold artifacts while still preserving a
clear gate for every promoted task.

## Commands

```bash
python3 runners/materialize_vabench_main_seed.py --output-bench benchmark-vabench-main-v1 --force
python3 runners/audit_bpack_semantic_contracts.py --bench-dir benchmark-vabench-main-v1 --output-dir analysis
python3 runners/audit_vabench_benchmark_integrity.py --bench-dir benchmark-vabench-main-v1 --output-dir analysis
python3 runners/audit_vabench_result_reuse.py \
  --bench-dir benchmark-vabench-main-v1 \
  --result-dir results/vabench-main-v1-draft7-gold-evas-2026-05-08 \
  --output analysis/vabench-main-v1_draft7_reuse_hash_audit_20260508.json

python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft11-new4 \
  --backend evas \
  --task <new-or-changed-task-id> ... \
  --output-dir results/vabench-main-v1-draft11-new4-gold-evas-2026-05-08 \
  --timeout-s 180

python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft11-new4 \
  --backend spectre \
  --task <new-or-changed-task-id> ... \
  --output-dir results/vabench-main-v1-draft11-new4-gold-spectre-jin-2026-05-08 \
  --timeout-s 180 \
  --env /Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite/.env \
  --profile jin
```

## Promotion State

| Gate | Status |
| --- | --- |
| Four task forms per promoted pack | PASS: 11/11 packs |
| Semantic audit hard FAIL | PASS: 0 hard FAIL |
| Benchmark integrity audit | PASS |
| Gold strict-EVAS evidence | PASS: composed 44/44 |
| Gold Spectre evidence | PASS: composed 44/44 |
| Full `vaBench-main-v1` coverage | IN PROGRESS: 11/30 packs |

## Remaining Risks

| Risk | Mitigation |
| --- | --- |
| Incremental validation may miss accidental old-task file changes if change detection is manual | Keep full semantic/integrity audit mandatory; before benchmark freeze, run full EVAS/Spectre once |
| EVAS/Spectre parity can drift after kernel or preflight changes | Treat any validator/kernel/preflight change as a full rerun trigger |
| 44 tasks are still not enough for final main benchmark claims | Continue pack expansion toward the planned 30-pack main set and reserve heldout packs |
