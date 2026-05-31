# Post-Asset-Repair EVAS and Baseline Audit

Date: `2026-05-27T08:15:57.505649+00:00`

This report is EVAS-only local consistency evidence plus an EVAS-filter rescore of existing DeepSeek candidates. Spectre remains the final judge and was not rerun in this pass because license checkout was blocked earlier.

## Full EVAS-Only Audit

| Metric | Value |
| --- | ---: |
| selected bundles | 325 |
| completed bundles | 325 |
| expected met | 325 |
| expected miss | 0 |
| raw status counts | `{'FAIL_SIM_CORRECTNESS': 54, 'PASS': 271}` |

## DeepSeek v4 Pro Rescore

| Metric | Value |
| --- | ---: |
| scored forms | 236 |
| EVAS pass count | 34 |
| EVAS pass@1 | 0.1441 |
| status counts | `{'PASS': 34, 'FAIL_DUT_COMPILE': 116, 'FAIL_SIM_CORRECTNESS': 69, 'FAIL_TB_COMPILE': 16, 'FAIL_INFRA': 1}` |
| selected issue signatures | `{'no_ahdl_va_include_in_tb': 57, 'dut_not_compiled': 104, 'tb_not_executed': 98, 'tran.csv missing': 106, 'missing_generated_files': 1}` |

### By Form

| Form | Pass | Total | Pass Rate |
| --- | ---: | ---: | ---: |
| `bugfix` | 11 | 52 | 0.2115 |
| `dut` | 19 | 52 | 0.3654 |
| `e2e` | 0 | 66 | 0.0 |
| `tb` | 4 | 66 | 0.0606 |

### By Difficulty

| Difficulty | Pass | Total | Pass Rate |
| --- | ---: | ---: | ---: |
| `D1` | 9 | 24 | 0.375 |
| `D2` | 24 | 180 | 0.1333 |
| `D3` | 1 | 32 | 0.0312 |

## Boundary

- This is not a Spectre certification update.
- Old dual-certification artifacts should not be treated as refreshed for files changed in this pass until Spectre rerun succeeds.
