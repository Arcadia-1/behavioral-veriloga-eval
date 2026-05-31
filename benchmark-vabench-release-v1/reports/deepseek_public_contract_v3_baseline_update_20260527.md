# DeepSeek public-contract-v3 Baseline Update

Date: 2026-05-27

This updates the DeepSeek v4-pro baseline against `public-contract-v3`.
It is an incremental baseline: `tb` and `e2e` were regenerated because their
public Spectre scaffold changed materially; `dut` and `bugfix` candidates were
reused from the previous DeepSeek run and re-scored with the current assets.

## Prompt-only EVAS baseline

| Metric | Old | New |
| --- | ---: | ---: |
| scored forms | 236 | 236 |
| EVAS pass | 34 | 46 |
| EVAS pass rate | 0.1441 | 0.1949 |

| Form | Source | Pass | Total | Pass rate |
| --- | --- | ---: | ---: | ---: |
| `bugfix` | reused previous candidates, re-scored | 11 | 52 | 0.2115 |
| `dut` | reused previous candidates, re-scored | 19 | 52 | 0.3654 |
| `e2e` | regenerated with public-contract-v3 | 6 | 66 | 0.0909 |
| `tb` | regenerated with public-contract-v3 | 10 | 66 | 0.1515 |

Generation status for the composed run: `generated=217`,
`no_code_extracted=19`.

## Spectre final judge

The effective dual confirmation used `thu-sui` as SSH jump host and `thu-wei`
as the Spectre compute host.

| Metric | Value |
| --- | ---: |
| EVAS-pass candidates selected | 48 |
| Spectre final pass | 46 |
| dual pass | 44 |
| EVAS PASS / Spectre FAIL | 2 |
| Spectre PASS / EVAS FAIL | 0 |

The 48 selected candidates came from the pre-fix EVAS filter. After the EVAS
syntax-compatibility fix and a clean-output re-score, the prompt-only EVAS
count is 46/236.

Two earlier attempts are not counted as final judge evidence:

- `thu-sui` compute attempt: Spectre started but waited on `5280@thu-han`;
  the short effective `+lqtimeout 270` produced `SPECTRE-209` license failures.
- sandboxed `thu-wei` attempt: SSH/control-socket access was blocked and remote
  workdir creation failed.

## EVAS false positives

| Task | Form | Cause |
| --- | --- | --- |
| `flash_adc_3b_smoke` | `e2e` | Candidate declares and initializes `real` variables inside an event block; EVAS accepted it, Spectre rejected it. |
| `vbr1_l1_pipeline_adc_stage_tb` | `tb` | Candidate uses multiline Spectre `vsource type=pwl wave=[...]`; EVAS accepted it, Spectre rejected it. |

These two cases are now rejected by EVAS locally: `flash_adc_3b_smoke` fails at
DUT compile because of a local declaration inside an event block, and
`vbr1_l1_pipeline_adc_stage_tb` fails at TB compile because the implicit
multiline PWL block lacks Spectre backslash continuation.

Conservative reporting should use 46/236 Spectre-confirmed passes for model
capability. The historical 48-selected dual artifact is preserved as diagnostic
evidence for the compatibility bug that has now been fixed.

## Artifacts

- Prompt-only summary: `results/vabench-release-v1-baseline-deepseek-v4-pro-20260527-public-contract-v3-incremental/summary.json`
- Composition report: `results/vabench-release-v1-baseline-deepseek-v4-pro-20260527-public-contract-v3-incremental/baseline_composition.json`
- Effective dual summary: `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260527-public-contract-v3-incremental-evas-pass-thu-wei-full/summary.json`
- Runner change: `runners/run_gold_dual_suite.py` now honors `VAEVAS_SUI_PROXY_JUMP` for `sui-direct` SSH.
