# bpack-v1 Materialization Report

**Date**: 2026-05-07

## Summary

| item | value |
| --- | ---: |
| inventory packs | 12 |
| materialized tasks | 41 |
| complete referenced packs | 8 |
| exact seed packs | 4 |
| strict-EVAS gold pass | 41/41 |

The materialized root is `benchmark-bpack-v1/`.  It is runnable and all currently materialized gold tasks pass strict-EVAS.  It is still a draft because only 41 of the target 48 tasks exist and several complete packs still require contract review before benchmark freeze.

## Form Coverage

| form | materialized tasks | target | missing |
| --- | ---: | ---: | ---: |
| `bugfix` | 9 | 12 | 3 |
| `spec-to-va` | 11 | 12 | 1 |
| `end-to-end` | 12 | 12 | 0 |
| `tb-generation` | 9 | 12 | 3 |

## Pack Status

| pack | inventory status | materialized | strict-EVAS gold | missing forms | next action |
| --- | --- | ---: | ---: | --- | --- |
| `threshold_detector` | `existing_exact_pack` | 4/4 | 4/4 | - | Promote after optional Spectre audit. |
| `window_detector` | `existing_exact_pack` | 4/4 | 4/4 | - | Promote after optional Spectre audit. |
| `analog_limiter` | `existing_exact_pack` | 4/4 | 4/4 | - | Promote after optional Spectre audit. |
| `pulse_stretcher` | `existing_exact_pack` | 4/4 | 4/4 | - | Promote after optional Spectre audit. |
| `sample_hold` | `existing_needs_contract_review` | 4/4 | 4/4 | - | Review same-function contract, then promote or split. |
| `pfd_updn` | `existing_needs_contract_review` | 4/4 | 4/4 | - | Review same-function contract, then promote or split. |
| `binary_dac_4b` | `existing_needs_contract_review` | 4/4 | 4/4 | - | Review same-function contract, then promote or split. |
| `clock_divider` | `needs_authoring` | 3/4 | 3/3 | `bugfix` | Author missing forms, then rerun gold validation. |
| `hysteresis_comparator` | `needs_authoring` | 3/4 | 3/3 | `tb-generation` | Author missing forms, then rerun gold validation. |
| `flash_adc_3b` | `needs_authoring` | 1/4 | 1/1 | `bugfix`, `spec-to-va`, `tb-generation` | Author missing forms, then rerun gold validation. |
| `dwa_pointer` | `needs_authoring` | 4/4 | 4/4 | - | Split/re-author to one concrete function pack. |
| `prbs7_lfsr` | `needs_authoring` | 2/4 | 2/2 | `bugfix`, `tb-generation` | Author missing forms, then rerun gold validation. |

## Validation Artifacts

- EVAS result root: `results/bpack-v1-draft-gold-evas-2026-05-07-r2/`
- Benchmark manifest: `benchmark-bpack-v1/manifest.json`
- Materializer: `runners/materialize_bpack_v1.py`

## Important Implementation Note

The materializer preserves `source_task_id` for legacy behavior checkers and records the copied benchmark-balanced task as `bpack_source_task_id`.  This matters because imported original-92 checkers use `source_task_id` to route into `simulate_evas.evaluate_behavior`.

## Next Work Before Model Runs

1. Freeze the four exact seed packs or run a targeted Spectre audit on them.
2. Decide whether `sample_hold`, `pfd_updn`, and `binary_dac_4b` are truly same-function packs.
3. Author the 7 missing forms for `clock_divider`, `hysteresis_comparator`, `flash_adc_3b`, and `prbs7_lfsr`.
4. Split or re-author `dwa_pointer`, because the current four referenced tasks mix calibration and DWA pointer contracts.
