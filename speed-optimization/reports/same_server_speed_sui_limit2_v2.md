# Same-Server EVAS/Spectre Speed

Date: 2026-05-21
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host, but this lightweight harness only validates Spectre returncode/log success. Paper-facing claims still need waveform/checker validation and repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 2
- EVAS modes: `strict_current, profile_fast_skip_source_error_control`
- Spectre modes: `ax, classic`
- Output root: `results/same-server-speed-sui-limit2-v2-20260521`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 2 | 1 | 1 | 18.532 | 9.266 |
| evas | strict_current | 2 | 1 | 1 | 250.075 | 125.038 |
| spectre | ax | 2 | 2 | 0 | 19.108 | 9.554 |
| spectre | classic | 2 | 2 | 0 | 88.215 | 44.107 |

## Per-Row Speedups

| Entry | Form | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_gain_estimator` | `e2e` | `ax` | `profile_fast_skip_source_error_control` | 9.319 | 9.434 | 0.988 |
| `vbr1_l1_gain_estimator` | `e2e` | `ax` | `strict_current` | 9.319 | 127.015 | 0.073 |
| `vbr1_l1_gain_estimator` | `e2e` | `classic` | `profile_fast_skip_source_error_control` | 44.294 | 9.434 | 4.695 |
| `vbr1_l1_gain_estimator` | `e2e` | `classic` | `strict_current` | 44.294 | 127.015 | 0.349 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `ax` | `profile_fast_skip_source_error_control` | 9.789 | 9.099 | 1.076 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `ax` | `strict_current` | 9.789 | 123.060 | 0.080 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `classic` | `profile_fast_skip_source_error_control` | 43.921 | 9.099 | 4.827 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `classic` | `strict_current` | 43.921 | 123.060 | 0.357 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- This harness does not replace EVAS/Spectre waveform parity certification.
