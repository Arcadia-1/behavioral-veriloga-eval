# MiMo P0 Contract And Checker Rerun - 2026-05-29

Scope: 40 previously audited MiMo rows affected by public prompt contract or release checker selection fixes.

## Fixes Applied Before Rerun

- Added public stimulus schedule contracts to 32 affected `tb`/`e2e` prompts.
- Fixed release checker selection so rows with legacy `meta.id` still resolve to release checker aliases.
- Fixed dual-run classification so Spectre backend/SSH failures are marked inconclusive, not counted as `EVAS PASS / Spectre FAIL`.

Task list:

- `benchmark-vabench-release-v1/reports/mimo_p0_contract_checker_rerun_task_ids_20260529.txt`
- `benchmark-vabench-release-v1/reports/mimo_p0_contract_checker_rerun_manifest_20260529.json`

## MiMo Generation And EVAS Result

Result root:

- `results/vabench-release-v1-baseline-minimax-mimo-v2.5-pro-20260529-mimo-p0-contract-checker-rerun40-direct`

Summary:

| Metric | Value |
| --- | ---: |
| selected rows | 40 |
| generated | 40 |
| EVAS pass | 28 |
| EVAS fail | 12 |

Compared with the earlier full236 MiMo EVAS run, the same 40-row slice changed from `1/40` EVAS pass to `28/40` EVAS pass. This is evidence that the prompt-contract/checker fixes matter, but it is not a final Spectre baseline update.

By form:

| Form | Pass | Total |
| --- | ---: | ---: |
| `tb` | 21 | 21 |
| `e2e` | 6 | 11 |
| `dut` | 1 | 4 |
| `bugfix` | 0 | 4 |

EVAS failures after rerun:

| Task | EVAS Status | Short Reason |
| --- | --- | --- |
| `vbr1_l1_higher_order_filter:e2e` | `FAIL_SIM_CORRECTNESS` | two-pole output stayed at reset level |
| `vbr1_l1_ldo_regulator_macro_model:dut` | `FAIL_SIM_CORRECTNESS` | metric did not distinguish heavy load/recovery |
| `vbr1_l1_limiting_amplifier_frontend:e2e` | `FAIL_DUT_COMPILE` | generated DUT did not compile |
| `vbr1_l1_offset_comparator:bugfix` | `FAIL_DUT_COMPILE` | generated fix did not compile |
| `vbr1_l1_programmable_gain_amplifier:dut` | `FAIL_DUT_COMPILE` | generated DUT did not compile |
| `vbr1_l1_resettable_integrator:bugfix` | `FAIL_SIM_CORRECTNESS` | integrator did not integrate/restart |
| `vbr1_l1_resettable_integrator:dut` | `FAIL_SIM_CORRECTNESS` | integrator did not integrate/restart |
| `vbr1_l1_resettable_integrator:e2e` | `FAIL_SIM_CORRECTNESS` | integrator did not integrate/restart |
| `vbr1_l1_slew_rate_limiter:bugfix` | `FAIL_DUT_COMPILE` | generated fix did not compile |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `FAIL_DUT_COMPILE` | generated fix did not compile |
| `vbr1_l1_thermometer_code_decoder:e2e` | `FAIL_DUT_COMPILE` | generated DUT did not compile |
| `vbr1_l2_iq_downconversion_chain:e2e` | `FAIL_SIM_CORRECTNESS` | positive quadrature behavior missing |

## Spectre Dual Status

Classified dual result root:

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-mimo-p0-contract-checker-rerun40-direct-dual-classified`

Summary:

| Metric | Value |
| --- | ---: |
| completed dual rows | 40 |
| Spectre backend inconclusive | 40 |
| strict dual pass | 0 |
| EVAS PASS / Spectre FAIL | 0 |
| Spectre PASS / EVAS FAIL | 0 |

Reason: SSH to the direct-SUI Spectre backend failed before remote workdir creation, e.g. `remote_workdir_create_failed rc=255` / `remote_workdir_unresolved`. Independent smoke tests to `thu-sui`, `thu-wei`, and the public IP endpoint timed out from the current execution environment. Therefore this rerun updates MiMo generation/EVAS evidence only; strict Spectre-final baseline remains pending until backend connectivity is restored.
