# vaBench-main-v1 Draft4 Validation Report

**Date**: 2026-05-08

This report records the first expanded executable batch for `vaBench-main-v1`:
4 circuit-function packs x 4 task forms = 16 tasks.  It extends the original
2-pack seed with two threshold/static nonlinear packs while preserving the
30-pack / 120-task target for the final main benchmark.

## Benchmark Root

```text
benchmark-vabench-main-v1/
```

Current draft packs:

| Pack | Forms | Mechanism family | Source basis | Gate status |
| --- | ---: | --- | --- | --- |
| `offset_comparator` | 4 | threshold/static nonlinear | adapted from `original92_comparator_offset_tb` | PASS |
| `strongarm_comparator_behavior` | 4 | threshold/static nonlinear | `original92_cmp_strongarm_smoke`, `original92_strongarm_reset_priority_bug` | PASS |
| `pfd_reset_race` | 4 | event/timing | `original92_pfd_reset_race_smoke` | PASS |
| `voltage_clamp` | 4 | threshold/static nonlinear | adapted from `balanced_analog_limiter_*`, rewritten as a non-duplicate clamp interface | PASS |

## Materialization

Script:

```text
runners/materialize_vabench_main_seed.py
```

Command:

```bash
python3 runners/materialize_vabench_main_seed.py --force
```

Result:

| Packs | Tasks | Forms per pack |
| ---: | ---: | ---: |
| 4 | 16 | 4 |

## Semantic Audit

Command:

```bash
python3 runners/audit_bpack_semantic_contracts.py \
  --bench-dir benchmark-vabench-main-v1 \
  --output-dir analysis
```

Result:

| Audit | PASS | WARN | FAIL |
| --- | ---: | ---: | ---: |
| draft4 semantic audit | 16 | 0 | 0 |

All draft4 tasks now use benchmark-local public checker logic.  The previous source-task checker routing warnings were removed before rerunning EVAS/Spectre.

Artifacts:

```text
analysis/vabench-main-v1_semantic_contract_audit_20260508.md
analysis/vabench-main-v1_semantic_contract_audit_20260508.json
```

## Gold strict-EVAS

Command:

```bash
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft4 \
  --backend evas \
  --output-dir results/vabench-main-v1-draft4-publiccheckers-gold-evas-2026-05-08 \
  --timeout-s 180
```

Result:

| Validator | PASS | Failure taxonomy |
| --- | ---: | --- |
| strict-EVAS | 16/16 | none |

Artifact:

```text
results/vabench-main-v1-draft4-publiccheckers-gold-evas-2026-05-08/summary.json
```

## Gold Spectre

Command:

```bash
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-draft4 \
  --backend spectre \
  --output-dir results/vabench-main-v1-draft4-publiccheckers-gold-spectre-jin-2026-05-08 \
  --timeout-s 180 \
  --env /Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite/.env \
  --profile jin
```

Bridge route:

```text
local -> thu-jin -> thu-wei
```

Result:

| Validator | PASS | Failure taxonomy |
| --- | ---: | --- |
| Spectre | 16/16 | none |

Artifact:

```text
results/vabench-main-v1-draft4-publiccheckers-gold-spectre-jin-2026-05-08/summary.json
```

## Promotion State

| Gate | Status |
| --- | --- |
| Four task forms per promoted pack | PASS |
| Semantic audit hard FAIL | PASS: 0 hard FAIL |
| Gold strict-EVAS | PASS: 16/16 |
| Gold Spectre | PASS: 16/16 |
| Full `vaBench-main-v1` coverage | IN PROGRESS: 4/30 packs |

## Next Expansion Batch

Recommended next packs:

1. `track_hold_aperture`: stateful analog memory; adapts existing sample-hold/aperture evidence.
2. `edge_detector`: event/timing; adapts existing edge/pulse families.
3. `resettable_counter_divider`: event/timing; adapts existing divider/counter evidence.
4. `sar_logic_4b`: data conversion; begins covering non-threshold families.

Keep weak-candidate packs out of the automated path until each has a manually
reviewed public prompt/checker/gold contract.
