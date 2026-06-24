# Spectre v2 Five-Task Review

Date: 2026-06-24

Scope: fresh Spectre/EVAS review for the five current vaBench release-v2 pilot
tasks, plus minimal Spectre probes for issues exposed by the DeepSeek v4 Flash
prompt smoke.

Bridge evidence:

- Bridge profile: `ci`
- Cadence setup: `/home/cshrc/.cshrc.cadence.IC618SP201`
- Spectre mode: `ax`
- Local raw evidence root for this run:
  `/private/tmp/vabench_v2_spectre_review_20260624`

Reproducibility note: this is a historical Spectre review summary. Issue #20
identified that the checked-in EVAS-only path did not reproduce the weighted-SAR
PASS from current code because the checker sampled intermediate SAR trial states
as final conversions. The post-fix EVAS-only reproduction is recorded in
`reports/spectre_mini_cert/gold_evas_only_cert_issue20_fix_20260624.md`.

## Fresh v2 Gold Dual Rerun

All five v2 gold/reference forms passed EVAS, Spectre, behavior checking, and
parity on the staged v2 assets.

| Task | EVAS | Spectre | Behavior | Parity |
| --- | --- | --- | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | PASS | PASS | 1.0 | passed |
| `vbr1_l1_window_comparator_detector:tb` | PASS | PASS | 1.0 | passed |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | PASS | PASS | 1.0 | passed |
| `vbr1_l1_first_order_lowpass:bugfix` | PASS | PASS | 1.0 | passed |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | PASS | PASS | 1.0 | passed |

Result: the five v2 examples are self-contained enough for fresh gold
dual-certification smoke. This does not certify the lost DeepSeek candidate
outputs; those exact candidate directories were not present under `/private/tmp`
when this review started.

## Spectre Probe Findings

| Probe | Spectre result | Classification |
| --- | --- | --- |
| CT02 multiline `wave=[...]` without backslash continuation | FAIL, `SFE-874` unexpected end of line | Real Spectre syntax failure; public TB spec should require one-line PWL arrays or backslash continuation. |
| CT02 multiline `wave=[...]` with backslash continuation | PASS | Confirms the prompt/spec repair path. |
| CT04 `laplace_nd()` low-pass implementation | PASS | EVAS compatibility debt; do not permanently prompt-ban Spectre-legal Laplace low-pass forms. |
| CT04 `last_crossing()` inside conditional/event expression | FAIL, `VACOMP-2144` | Real Spectre restriction for this usage form; keeping a low-pass-task guard is reasonable. |
| CT04 local `real` declaration inside an unlabeled event block | FAIL, `VACOMP-1917` | Real Spectre restriction; module-scope declaration guidance is justified. |
| CT04 runtime variable as periodic `timer(0, dt)` period | PASS | EVAS event lowering debt; do not permanently prompt-ban Spectre-legal dynamic timer periods. |

## Fixes Applied From This Review

- CT02 public spec now explicitly requires Spectre line continuation when a PWL
  `wave=[...]` array spans multiple physical lines.
- CT02 private checker config notes the same Spectre syntax requirement without
  imposing exact breakpoints or a fixed PWL template.
- CT04 public spec no longer bans Laplace low-pass operators or dynamic timer
  periods solely because current EVAS has limitations there.
- CT04 private checker config no longer rejects `laplace_` syntactically.

## Remaining Review Gaps

The exact DeepSeek candidate outputs from the earlier pilot were ephemeral and
not available for this rerun. Therefore:

- CT01 candidate `too_few_completed_conversions=0` remains unclassified for the
  exact generated artifact.
- SUP01 candidate EVAS Rust runtime failure remains unclassified for the exact
  generated artifact.
- CT03 and CT04 model-candidate Spectre confirmation also remains pending for
  the exact generated artifacts.

Next durable fix: make the model-smoke script copy extracted candidate files and
compact score summaries into `benchmark-vabench-release-v2/reports/model_smoke/`
or another intentional evidence directory before deleting `/private/tmp`.
