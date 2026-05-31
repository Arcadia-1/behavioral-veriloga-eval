# DeepSeek Current Success and Error Summary - 2026-05-28

This file records only valid DeepSeek v4-pro results. Failed API/proxy runs,
sandbox-blocked SSH runs, and `thu-sui` Spectre license-checkout failures are
excluded from all success-rate and error-rate tables.

## Authoritative Full-Release Result

Use this as the current full 236-form DeepSeek baseline until a new full-release
regeneration is run.

Sources:
- Prompt/EVAS score:
  `results/vabench-release-v1-baseline-deepseek-v4-pro-20260527-public-contract-v3-incremental/summary.json`
- Spectre confirmation of EVAS-selected candidates:
  `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260527-public-contract-v3-incremental-evas-pass-thu-wei-full/summary.json`

Scope:
- Model: `deepseek-v4-pro`
- Benchmark denominator: 236 scored forms
- Prompt version: `public-contract-v3`
- Spectre compute: `thu-wei`

| Metric | Count | Rate | Use |
| --- | ---: | ---: | --- |
| Spectre-final model pass | 46 / 236 | 19.49% | Main current DeepSeek score |
| EVAS-filter pass | 46 / 236 | 19.49% | Fast-filter diagnostic only |
| EVAS/Spectre clean dual pass | 44 / 236 | 18.64% | EVAS parity diagnostic |
| EVAS PASS / Spectre FAIL | 2 / 236 | 0.85% | EVAS over-admission cases |
| Spectre PASS / EVAS FAIL | 0 / 236 | 0.00% | No observed missed Spectre pass |

Important distinction:
- **Model score:** use Spectre-final pass, `46/236`.
- **EVAS parity score:** use clean dual pass, `44/236`.
- The two are different because two Spectre-passing candidates had waveform
  parity issues, and two EVAS-passing candidates failed Spectre.

### Full-Release Success By Form

These counts use the current Spectre-final model-pass number where available.

| Form | Spectre-Final Pass | Total | Rate |
| --- | ---: | ---: | ---: |
| `dut` | 19 | 52 | 36.54% |
| `bugfix` | 11 | 52 | 21.15% |
| `tb` | 10 | 66 | 15.15% |
| `e2e` | 6 | 66 | 9.09% |

### Full-Release Error Types

These are EVAS scoring statuses over all 236 forms. They are useful for error
analysis, but Spectre remains the final judge for pass claims.

| Status | Count | Meaning |
| --- | ---: | --- |
| `FAIL_SIM_CORRECTNESS` | 106 | Candidate reached behavior checking but failed the checker. |
| `FAIL_DUT_COMPILE` | 50 | Generated DUT/fix did not compile or could not be staged as a valid DUT. |
| `FAIL_INFRA` | 23 | Missing generated artifact, no extracted code, or scoring/staging failure. |
| `FAIL_TB_COMPILE` | 11 | Generated Spectre testbench failed compile/run. |

### Full-Release EVAS/Spectre Exceptions

These four rows are valid diagnostic evidence from the full-release dual run.
They are not external infrastructure failures.

| Task | Form | Dual Status | Interpretation |
| --- | --- | --- | --- |
| `flash_adc_3b_smoke` | `e2e` | `FAIL_SPECTRE` | EVAS accepted the candidate, but Spectre rejected it. |
| `vbr1_l1_pipeline_adc_stage_tb` | `tb` | `FAIL_SPECTRE` | EVAS accepted the candidate, but Spectre rejected it. |
| `vbr1_l1_clocked_sample_and_hold_e2e` | `e2e` | `FAIL_PARITY` | Spectre checker passed, but waveform parity failed. |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap_dut` | `dut` | `FAIL_PARITY` | Spectre checker passed, but waveform parity failed. |

## Valid Targeted L1/L2 Prompt-Sufficiency Slice

This is a local rerun only for forms touched by the recent L1/L2 prompt
sufficiency repair. Do not use it as a new full-release success rate.

Sources:
- Rerun manifest:
  `benchmark-vabench-release-v1/reports/prompt_sufficiency_l1_l2_rerun_manifest_20260527.json`
- Prompt/EVAS score:
  `results/vabench-release-v1-baseline-minimax-deepseek-v4-pro-20260527-public-contract-v7-l1-l2-prompt-sufficiency-slice-r2/summary.json`
- Spectre confirmation:
  `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260527-public-contract-v7-l1-l2-prompt-sufficiency-slice-r2-evas-pass-thu-wei/summary.json`

Scope:
- Model: `deepseek-v4-pro`
- Denominator: 40 changed forms only
- Spectre compute: `thu-sui -> thu-wei`

| Metric | Count | Rate |
| --- | ---: | ---: |
| Generated candidates | 34 / 40 | 85.00% |
| No code extracted | 6 / 40 | 15.00% |
| EVAS-filter pass | 7 / 40 | 17.50% |
| Spectre-final pass | 7 / 40 | 17.50% |
| EVAS PASS / Spectre FAIL | 0 / 7 | 0.00% |

### Targeted Slice Success By Form

| Form | Spectre-Final Pass | Total | Rate |
| --- | ---: | ---: | ---: |
| `tb` | 5 | 18 | 27.78% |
| `e2e` | 2 | 17 | 11.76% |
| `bugfix` | 0 | 5 | 0.00% |

### Targeted Slice Error Types

| Status | Count | Meaning |
| --- | ---: | --- |
| `FAIL_SIM_CORRECTNESS` | 17 | Candidate compiled/ran but failed behavior checks. |
| `FAIL_INFRA` | 9 | Mostly no extracted code or missing generated artifact. |
| `FAIL_TB_COMPILE` | 6 | Generated testbench failed compile/run. |
| `FAIL_DUT_COMPILE` | 1 | Generated DUT failed compile. |

## Excluded Runs

The following runs are not counted anywhere above:

| Run | Reason Excluded |
| --- | --- |
| `20260527-public-contract-v7-l1-l2-prompt-sufficiency-slice` | API calls went through a dead local proxy at `127.0.0.1:7897`; no valid candidates were generated. |
| `20260527-public-contract-v7-l1-l2-prompt-sufficiency-slice-r2-evas-pass` | Local sandbox blocked SSH with `Operation not permitted`; not a Spectre result. |
| `20260527-public-contract-v7-l1-l2-prompt-sufficiency-slice-r2-evas-pass-sui` | Ran on `thu-sui` and hit `SPECTRE-209` license checkout failure; not a model or benchmark failure. |
| `20260527-public-contract-v7-l1-l2-prompt-sufficiency-slice-r2-evas-pass-sui-lq1200` | Superseded after switching compute to `thu-wei`; not used for final counts. |

## Current Bottom Line

- Current full-release DeepSeek v4-pro score: **46/236 = 19.49% Spectre-final
  pass**.
- Current clean EVAS/Spectre dual pass on the full-release EVAS-selected set:
  **44/236 = 18.64%**.
- Current targeted L1/L2 prompt-sufficiency slice: **7/40 = 17.50%
  Spectre-final pass**, with **0 EVAS PASS / Spectre FAIL** on that slice.
- The dominant full-release failure type is still behavioral correctness
  failure, not merely testbench syntax.
