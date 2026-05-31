# EVAS / Spectre Precision-Ranking Experiment Tracker

Date: 2026-05-26

| Run ID | Milestone | Purpose | Systems / Variants | Rows | Metrics | Priority | Status | Notes |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| PR001 | M0 | Settings-normalization pilot | `spectre/classic`, `spectre/ax_speed`, `spectre/ax_normalized`, `spectre/reference_strict_primary` | 10 | behavior PASS, final command/options/tran manifest, accepted steps | MUST | TODO | Include simple, DAC, PFD, PLL, gain-estimator rows. |
| PR002 | M1 | Normalized ax-mode vs strict reference | `spectre/ax_normalized` vs `spectre/reference_strict_primary` | 259 | behavior PASS, relative RMS, absolute V, event/digital mismatch | MUST | TODO | One repeat first; do not use `ax_speed` for precision ranking. |
| PR003 | M1 | Current classic diagnostic vs strict reference | `spectre/classic` vs `spectre/reference_strict_primary` | 259 | same as PR002 | SHOULD | TODO | Diagnostic only; not part of settings-normalized precision ranking unless we add a separate normalized classic mode. |
| PR004 | M2 | EVAS strict vs strict reference | `evas/strict_current` vs `spectre/reference_strict_primary` | 259 | behavior PASS, equivalence gate, waveform metrics | MUST | TODO | Establish EVAS internal reference distance. |
| PR005 | M2 | EVAS fast vs strict reference | `evas/profile_fast_skip_source_error_control` vs `spectre/reference_strict_primary` | 259 | behavior PASS, equivalence gate, waveform metrics | MUST | TODO | Main test for fast-profile precision loss. |
| PR006 | M3 | Precision-ranking aggregate | `spectre/ax_normalized`, `evas/strict_current`, `evas/fast` all vs strict reference | matched rows | PASS count, worst-signal relative RMS, row-mean relative RMS, max RMS V | MUST | TODO | Determines allowed paper wording. |
| PR007 | M4 | Same-server speed rerun with refined labels | `spectre/ax_speed`, `spectre/classic`, `evas/strict_current`, `evas/fast` | 259 x 4 repeats | geomean/median/min/max speedup, PASS count | MUST | TODO | Keep same host and worker count as previous speed result. |
| PR008 | M5 | Half-step sensitivity pilot | `spectre/reference_strict_primary`, `spectre/reference_strict_halfstep`, EVAS fast | 30 | waveform metrics, checker stability, runtime blow-up | NICE | TODO | Appendix only unless it changes conclusions. |
