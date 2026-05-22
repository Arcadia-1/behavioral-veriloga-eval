# Same-Server Reproducibility Fix Analysis

Date: 2026-05-22

## Scope

This note summarizes the local-to-`thu-sui` reproducibility fix for the same-server EVAS/Spectre speed runner.

Primary artifacts:

- `fixture_materialization_audit_sui_20260522.json`
- `same_server_speed_sui_repro_smoke_20260522.json`
- `same_server_speed_sui_repro_full_v3_20260522.json`

## Runner Changes

- Materialize runnable fixtures instead of copying only the selected form's `gold/` directory.
- Reuse sibling `tb`/`e2e` testbenches when `dut` or `bugfix` forms are not standalone.
- Copy the selected form's Verilog-A source back over the staged fixture so the candidate under test remains the selected form.
- Materialize missing `ahdl_include` files from current or sibling gold directories.
- For `bugfix`, only the first DUT include may be replaced by `dut_fixed.va` or `dut_buggy.va`; auxiliary includes are not overwritten by the variant source.
- Include `entry_id/form/variant/task_id` in output paths and accuracy grouping to avoid collisions between variants or duplicate task ids.
- Add `--audit-fixtures-only` so local and server fixture reproducibility can be checked without running simulators.

## Validation Evidence

| Check | Result |
| --- | ---: |
| Local `py_compile` | PASS |
| Local fixture audit | 259 / 259 PASS |
| `thu-sui` `py_compile` | PASS |
| `thu-sui` fixture audit | 259 / 259 PASS |
| `thu-sui` smoke run | 4 rows, 12 / 12 backend-mode jobs PASS |
| `thu-sui` full-v3 run | 259 rows, 1036 / 1036 backend-mode jobs produced simulation output |
| File-related full-v3 errors | 0 |

File-related checks in full-v3 all stayed at zero: `FileNotFoundError`, missing included files, missing gold testbench, missing `ahdl_include`, and missing CSV.

## Full-v3 Mode Summary

| Backend | Mode | Runs | Behavior PASS | Non-PASS | Mean wall s | Geomean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| EVAS | `profile_fast_skip_source_error_control` | 259 | 235 | 24 | 1.639 | 1.173 |
| EVAS | `strict_current` | 259 | 235 | 24 | 5.565 | 1.921 |
| Spectre | `ax` | 259 | 235 | 24 | 8.076 | 7.608 |
| Spectre | `classic` | 259 | 235 | 24 | 24.930 | 23.858 |

The 24 non-PASS rows are not fixture failures. They are rows without behavior checkers, so the accuracy gate marks them `BLOCKED` instead of `FAIL`.

## Accuracy Gate

| EVAS mode | Runs | PASS | FAIL | BLOCKED |
| --- | ---: | ---: | ---: | ---: |
| `profile_fast_skip_source_error_control` | 259 | 235 | 0 | 24 |
| `strict_current` | 259 | 235 | 0 | 24 |

Blocked reason counts:

- `candidate_no_behavior_checker`: 48 EVAS results
- `spectre_ax_parity:spectre_no_behavior_checker`: 48 EVAS results
- `spectre_classic_parity:spectre_no_behavior_checker`: 48 EVAS results

## Speed Summary

Accuracy-gated geomean Spectre/EVAS speedup across all selected pairs: **9.229x**.

| Spectre mode | EVAS mode | Accuracy-gated rows | Geomean Spectre/EVAS |
| --- | --- | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 235 | 6.566x |
| `ax` | `strict_current` | 235 | 4.229x |
| `classic` | `profile_fast_skip_source_error_control` | 235 | 20.139x |
| `classic` | `strict_current` | 235 | 12.973x |

These are same-server single-run numbers. Paper-facing speed claims should still separate cold/warm cache behavior and use repeated runs.

## Interpretation

The previous server mismatch was a benchmark packaging/materialization issue, not evidence that the server could not reproduce local EVAS behavior. After the fix, the clean server workdir can reconstruct runnable fixtures for all selected rows and run both EVAS and Spectre without missing-file errors.

Remaining work is now narrower:

- Add or repair behavior checkers for the 24 blocked rows.
- Repeat same-server timing with cold/warm cache controls before making final paper speed claims.
- Keep fixture audit in the benchmark release flow so future task additions cannot silently depend on local generated staging directories.
