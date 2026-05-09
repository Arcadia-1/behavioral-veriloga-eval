# vaBench-main-v1 Seed Validation Report

**Date**: 2026-05-08

This report records the first executable seed batch for `vaBench-main-v1`.  The
seed is deliberately small: 2 source-backed packs x 4 task forms = 8 tasks.  It
validates the authoring/materialization workflow before scaling to the full 30
pack / 120 task main benchmark.

## Seed Root

```text
benchmark-vabench-main-v1/
```

Current seed packs:

| Pack | Forms | Source basis | Status |
| --- | ---: | --- | --- |
| `strongarm_comparator_behavior` | 4 | `original92_cmp_strongarm_smoke`, `original92_strongarm_reset_priority_bug` | strict-EVAS gold PASS after per-form checker binding fix. |
| `pfd_reset_race` | 4 | `original92_pfd_reset_race_smoke` | strict-EVAS gold PASS; runtime is relatively slow because of the dense 300 ns PFD waveform. |

## Materialization

Script:

```text
runners/materialize_vabench_main_seed.py
```

Important fix discovered during validation:

- `strongarm_comparator_behavior_bugfix` must use source checker id
  `strongarm_reset_priority_bug`, not the e2e checker id `cmp_strongarm_smoke`.
- This caught exactly the kind of prompt/checker/gold mismatch that the benchmark
  gate is meant to prevent.

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
| seed semantic audit | 3 | 5 | 0 |

Artifact:

```text
analysis/vabench-main-v1_semantic_contract_audit_20260508.md
analysis/vabench-main-v1_semantic_contract_audit_20260508.json
```

Remaining WARNs are `checker_source_task_not_named`; they are acceptable for the
source-backed seed but should be minimized in newly authored packs.

## Gold strict-EVAS

Command:

```bash
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-seed \
  --backend evas \
  --output-dir results/vabench-main-v1-seed-gold-evas-2026-05-08-r2 \
  --timeout-s 180
```

Result:

| Validator | PASS | Notes |
| --- | ---: | --- |
| strict-EVAS | 8/8 | Gold gate passes for the seed batch. |

Artifact:

```text
results/vabench-main-v1-seed-gold-evas-2026-05-08-r2/summary.json
```

## Gold Spectre

Command:

```bash
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-vabench-main-v1 \
  --family vabench-main-v1-seed \
  --backend spectre \
  --output-dir results/vabench-main-v1-seed-gold-spectre-jin-2026-05-08 \
  --timeout-s 180 \
  --env /Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite/.env \
  --profile jin
```

Bridge route:

```text
local -> thu-jin -> thu-wei
```

The original default/ci bridge profiles are preserved.  The `jin` profile was
added for current vaEVAS Spectre audits and relies on the local SSH config where
`Host thu-wei` uses `ProxyJump thu-jin`.

| Validator | PASS | Notes |
| --- | ---: | --- |
| Spectre | 8/8 | Gold gate passes for the seed batch. |

Artifact:

```text
results/vabench-main-v1-seed-gold-spectre-jin-2026-05-08/summary.json
```

## Promotion State

| Gate | Status |
| --- | --- |
| Four task forms per seed pack | PASS |
| Semantic audit hard FAIL | PASS: 0 hard FAIL |
| Gold strict-EVAS | PASS: 8/8 |
| Gold Spectre | PASS: 8/8 |
| Full `vaBench-main-v1` coverage | NOT STARTED: seed only |

## Next Actions

1. Add gold runtime accounting to the promotion gate, because PFD dense timing is slow.
2. Promote the seed materialization pattern to the next `source_backed` and `adapt_existing` packs.
3. Continue authoring from `docs/VABENCH_MAIN_AUTHORING_QUEUE.md` in batches, not all 120 tasks at once.
