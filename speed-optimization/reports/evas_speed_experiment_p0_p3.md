# EVAS Speed Experiment P0-P3

Date: 2026-05-21
Claim allowed: `False`
Reason: EVAS-only speed experiments are candidate evidence; paper-facing speed claims require same-slice EVAS/Spectre timing.

This artifact evaluates EVAS speed optimization candidates while keeping
the current EVAS path as the strict baseline. Default-off fast paths are
not claimable unless they pass strict-EVAS waveform parity and behavior checks.

## P0 Existing Baseline

- Source: `benchmark-vabench-release-v1/reports/speed_debug_artifact.json`
- Caveat: existing artifact compares local EVAS wrapper timing with remote Spectre wrapper timing
- Existing status: `measured`
- Existing speed claim allowed: `False`

## Scope

- Selected rows: 2
- Modes: `strict_current, profile_fast, skip_source_error_control, profile_fast_skip_source_error_control`
- Output root: `results/evas-speed-p0-p3-pilot-20260521`

## Mode Summary

| Mode | Runs | PASS | Non-PASS | Wall s | Median speedup vs strict | Safe vs strict | Unsafe vs strict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| profile_fast | 2 | 2 | 0 | 25.962 | 2.6476972252182907 | 2 | 0 |
| profile_fast_skip_source_error_control | 2 | 2 | 0 | 21.423 | 3.053692255519059 | 2 | 0 |
| skip_source_error_control | 2 | 2 | 0 | 31.224 | 2.037307602277789 | 2 | 0 |
| strict_current | 2 | 2 | 0 | 119.915 | None | 0 | 0 |

## Safety Policy

- `strict_current` remains the certification baseline.
- P2 profiles are parameter ablations, not default behavior.
- P3 fast paths are default-off and must pass behavior and strict-EVAS waveform parity before promotion.
