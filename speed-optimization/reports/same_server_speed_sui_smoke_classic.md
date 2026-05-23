# Same-Server EVAS/Spectre Speed

Date: 2026-05-21
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host, but this lightweight harness only validates Spectre returncode/log success. Paper-facing claims still need waveform/checker validation and repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 1
- EVAS modes: `strict_current, profile_fast_skip_source_error_control`
- Spectre modes: `classic`
- Output root: `results/same-server-speed-sui-smoke-classic-20260521`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 1 | 1 | 0 | 15.531 | 15.531 |
| evas | strict_current | 1 | 1 | 0 | 32.715 | 32.715 |
| spectre | classic | 1 | 1 | 0 | 17.232 | 17.232 |

## Per-Row Speedups

| Entry | Form | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `classic` | `profile_fast_skip_source_error_control` | 17.232 | 15.531 | 1.109 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `classic` | `strict_current` | 17.232 | 32.715 | 0.527 |

## Interpretation Guardrails

- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- This harness does not replace EVAS/Spectre waveform parity certification.
