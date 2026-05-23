# Same-Server EVAS/Spectre Speed

Date: 2026-05-21
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host, but this lightweight harness only validates Spectre returncode/log success. Paper-facing claims still need waveform/checker validation and repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 1
- EVAS modes: `strict_current, profile_fast_skip_source_error_control`
- Spectre modes: `ax`
- Output root: `results/same-server-speed-sui-smoke-20260521`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 1 | 1 | 0 | 15.631 | 15.631 |
| evas | strict_current | 1 | 1 | 0 | 32.774 | 32.774 |
| spectre | ax | 1 | 1 | 0 | 4.418 | 4.418 |

## Per-Row Speedups

| Entry | Form | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `ax` | `profile_fast_skip_source_error_control` | 4.418 | 15.631 | 0.283 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `ax` | `strict_current` | 4.418 | 32.774 | 0.135 |

## Interpretation Guardrails

- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- This harness does not replace EVAS/Spectre waveform parity certification.
