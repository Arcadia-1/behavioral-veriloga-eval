# vaBench-main-v1 Draft7 Validation Report

**Date**: 2026-05-08

This report records the next benchmark expansion batch for `vaBench-main-v1`:
7 circuit-function packs x 4 task forms = 28 tasks.  The draft now covers
threshold/static nonlinear, event/timing, stateful analog memory, and data
conversion families.

## Benchmark Root

```text
benchmark-vabench-main-v1/
```

Current draft packs:

| Pack | Forms | Mechanism family | Source basis | Gate status |
| --- | ---: | --- | --- | --- |
| `offset_comparator` | 4 | threshold/static nonlinear | adapted from `original92_comparator_offset_tb` | PASS |
| `strongarm_comparator_behavior` | 4 | threshold/static nonlinear | `original92_cmp_strongarm_smoke`, `original92_strongarm_reset_priority_bug` | PASS |
| `voltage_clamp` | 4 | threshold/static nonlinear | adapted from `balanced_analog_limiter_*`, rewritten as clamp interface | PASS |
| `pfd_reset_race` | 4 | event/timing | `original92_pfd_reset_race_smoke` | PASS |
| `resettable_counter_divider` | 4 | event/timing | adapted from `original92_clk_divider` | PASS |
| `track_hold_aperture` | 4 | stateful analog memory | adapted from `original92_sample_hold_aperture_tb` | PASS |
| `sar_logic_4b` | 4 | data conversion | authored 4-bit SAR logic using original SAR mechanism as reference | PASS |

## Audit Gates

| Gate | Result | Artifact |
| --- | --- | --- |
| Semantic prompt/checker/gold audit | `28 PASS / 0 WARN / 0 FAIL` | `analysis/vabench-main-v1_semantic_contract_audit_20260508.json` |
| Benchmark integrity audit | `PASS`, no issues | `analysis/vabench-main-v1_integrity_audit_20260508.json` |
| Gold strict-EVAS | `28/28 PASS` | `results/vabench-main-v1-draft7-gold-evas-2026-05-08/summary.json` |
| Gold Spectre | `28/28 PASS` | `results/vabench-main-v1-draft7-gold-spectre-jin-2026-05-08/summary.json` |

## Commands

```bash
python3 runners/materialize_vabench_main_seed.py --force
python3 runners/audit_bpack_semantic_contracts.py --bench-dir benchmark-vabench-main-v1 --output-dir analysis
python3 runners/audit_vabench_benchmark_integrity.py --bench-dir benchmark-vabench-main-v1 --output-dir analysis
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft7 \
  --backend evas \
  --output-dir results/vabench-main-v1-draft7-gold-evas-2026-05-08 \
  --timeout-s 180
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft7 \
  --backend spectre \
  --output-dir results/vabench-main-v1-draft7-gold-spectre-jin-2026-05-08 \
  --timeout-s 180 \
  --env /Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite/.env \
  --profile jin
```

## Promotion State

| Gate | Status |
| --- | --- |
| Four task forms per promoted pack | PASS |
| Semantic audit hard FAIL | PASS: 0 hard FAIL |
| Benchmark integrity audit | PASS |
| Gold strict-EVAS | PASS: 28/28 |
| Gold Spectre | PASS: 28/28 |
| Full `vaBench-main-v1` coverage | IN PROGRESS: 7/30 packs |

## Current Coverage Gap

The benchmark is improved but still not ready for the main model matrix.  It now
has meaningful non-threshold coverage, but calibration/control, pointer/selection,
continuous dynamics, and source/measurement/TB families remain under-covered.

Recommended next expansion batch:

1. `one_shot_timer` or `edge_detector` for event/timing diversity beyond PFD/divider.
2. `thermometer_dac` or `segmented_dac` for data conversion beyond SAR logic.
3. `lock_detector` for calibration/control.
4. `resettable_integrator` for continuous dynamics.
