# D004 Bugfix Release Triage

Date: 2026-05-14; updated 2026-05-15

This table records the retained D004 bugfix provenance policy for the current
vaBench release: historical `bugfix` rows without current badcases should first
be reviewed for a reconstructable buggy source. A row remains release-facing
`bugfix` only after the reconstructed badcase fails and the fixed source passes
the public checker.

Release options:

- `B1 true-bugfix`: buggy source plus fixed source/contract are available or can
  be reconstructed as a small, realistic single-root-cause defect.
- `B1-reconstruct`: preferred next action for fixed-only historical bugfix rows
  whose intended defect can plausibly be recovered from the task semantics.
- `B2 behavior-regression`: no badcase is available; publish as a normal
  corrected behavior implementation task, with repair provenance retained in
  metadata.
- `B3 separate conformance asset`: the case is mainly about simulator/checker
  semantics such as event ordering, timer scheduling, final-step/file I/O,
  source boundary, or continuous-time operator handling. It moves to
  `conformance/evas-spectre/` and is excluded from normal vaBench task counts.
- `B4 evidence-only`: keep validation evidence internally until a reviewer
  approves B1/B2/B3.

Reconstruction gate:

- A B1 reconstruction needs a short dossier: one-root-cause diff, historical
  clue or rationale, why it is not only conformance, buggy/fixed EVAS evidence,
  buggy/fixed Spectre evidence, and reviewer signoff.
- For behavioral bugfixes, the buggy source must fail the public checker in
  both EVAS and Spectre, and the fixed source must pass both.
- For syntax bugfixes, record backend-specific compile expectations instead of
  forcing the buggy source to compile.
- A reconstructed badcase can modify one concept rather than literally one
  line, but the defect must remain minimal and plausible.

## First-Pass Triage

| Task ID | Evidence shape | Preferred action / fallback | Why | Reviewer question |
| --- | --- | --- | --- | --- |
| `vbm1_background_calibration_accumulator_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB, but duplicate kernel | B4 evidence-only until distinct defect exists | Same reset/clock/error/clamped-accumulator sign-reversal kernel as `vbm1_cdac_calibration_bugfix`; retaining both would over-count one repair pattern. | Keep evidence, exclude from bugfix/model counts, and redesign later only if a different realistic defect is needed. |
| `vbm1_barrel_pointer_window_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Wrong adjacent-window mapping duplicates `win1` and loses the wrap-around `3/0` window. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_cdac_calibration_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Wrong error-update direction is a plausible trim-controller repair defect and is distinct from full CDAC modeling. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_debounce_latch_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Rising-edge path bypasses the debounce timer and latches immediately, so the short-pulse window incorrectly sets `out`. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-batch3-*2026-05-14`. |
| `vbm1_edge_detector_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Wrong edge polarity triggers on falling edges instead of rising edges; this is a model-repair defect rather than timer conformance. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-pilot-*2026-05-14`. |
| `vbm1_element_shuffler_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Direct state-to-output mapping omits the intended shuffled output assignment, producing `2,1,3,0,2,1` instead of `1,2,3,0,1,2`. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-batch2-*2026-05-14`. |
| `vbm1_file_metric_writer_bugfix` | fixed DUT + TB plus output artifact; identical to the `_dut` staged fixture | B4 closed evidence-only; normal measurement task plus B3 conformance carry the useful semantics | Uses `$fopen/$fwrite` and a file artifact; current pass evidence mainly proves file/event/tool behavior plus `done` flag, not a repair. | Do not count historical row as bugfix. Ordinary `dut`/`tb`/`e2e` tasks are materialized; atomic file I/O stays in conformance. |
| `vbm1_first_order_lowpass_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source uses a too-small alpha, producing an unrealistically slow step response. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_gain_trim_controller_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source reverses the trim update direction, increasing error instead of correcting gain. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_leaky_hold_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source omits the leakage decay multiply, so held output stays high until reset. This is separate from atomic `$abstime` decay conformance. | EVAS and Spectre confirmed fixed-pass/buggy-fail on 2026-05-15. |
| `vbm1_lock_detector_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source asserts lock only after `streak > need`, delaying the lock indication by one qualified sample. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_offset_calibration_fsm_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source updates trim in the wrong direction during offset correction. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_offset_comparator_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source applies the offset with reversed polarity, flipping the threshold decisions. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_one_shot_timer_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + reset-during-pulse TB | B1-reconstructed | Buggy source omits the falling reset handler, so an active pulse waits for the timer instead of clearing immediately. | EVAS and Spectre confirmed fixed-pass/buggy-fail on 2026-05-15. |
| `vbm1_peak_detector_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source ignores reset, so a stale peak survives into the reset-clear window. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_pfd_reset_race_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | The DIV edge path forgets to clear both states when UP is already asserted; this creates a persistent UP/DN overlap. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-pilot-*2026-05-14`; EVAS needs a 300s timeout budget for this dense 10ps-step case. |
| `vbm1_precision_rectifier_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source behaves as an absolute-value rectifier, leaking negative half-cycle magnitude instead of producing zero. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_resettable_counter_divider_bugfix` | two reference-like DUTs + TB; identical to the `_dut` staged fixture | B4 closed evidence-only | Has `clk_divider.va` and `clk_divider_ref.va`, but the TB includes and instantiates only `clk_divider_ref`; `clk_divider.va` is an unused auxiliary/legacy source, not proven badcase evidence. | Do not count historical row as bugfix. Redesign a clean divider badcase later if this repair pattern is needed. |
| `vbm1_resettable_integrator_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source leaves stale accumulated state through reset, corrupting the post-reset integration window. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_rotating_element_selector_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Off-by-one wrap at `idx >= 3` skips selector state 3, producing `1,2,0,1,2,0` instead of `1,2,3,0,1,2`. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-batch2-*2026-05-14`. |
| `vbm1_sar_logic_4b_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source asserts `rdy` one SAR clock edge early, before the conversion-complete boundary. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_segmented_dac_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | The thermometer segment is weighted as two binary LSBs instead of four, compressing upper-code output levels. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-pilot-*2026-05-14`. |
| `vbm1_settling_time_measurement_tb_bugfix` | fixed DUT/TB measurement only; identical to the `_dut` staged fixture | B4 closed evidence-only; normal measurement task plus B3 conformance carry the useful semantics | Timer-driven first-order response and `done` threshold are measurement/testbench semantics rather than a DUT repair pair. | Do not count historical row as bugfix. Ordinary `dut`/`tb`/`e2e` tasks are materialized; boundary semantics stay in conformance. |
| `vbm1_slew_rate_limiter_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source limits only rising changes, allowing a falling step to exceed the configured slew bound. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |
| `vbm1_strongarm_comparator_behavior_bugfix` | `dut_buggy.va` + `dut_fixed.va` + TB | B1 | Explicit buggy/fixed pair; reset-priority defect is visible in source. | Keep as release-facing bugfix. |
| `vbm1_thermometer_dac_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed with semantic rename | Historical id says thermometer DAC, but the source is a 4-bit binary DAC. Endpoint scaling divides by 16 instead of 15, so full-scale code 15 never reaches `vref`. | Keep historical `task_id` for main120 traceability, but present/release this as a 4-bit binary DAC task. Add a separate true 15-segment thermometer DAC task later. |
| `vbm1_thermometer_decoder_guarded_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Binary code is decoded as one-hot rather than cumulative thermometer outputs. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-batch3-*2026-05-14`. |
| `vbm1_track_hold_aperture_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + aperture-discriminating TB | B1-reconstructed | Buggy source samples at the clock edge instead of at `clk+taperture`; the TB moves `vin` between those times and checks a later safe window. | EVAS and Spectre confirmed fixed-pass/buggy-fail on 2026-05-15. |
| `vbm1_vco_phase_integrator_bugfix` | fixed DUT + TB only; identical to the `_dut` staged fixture | B4 closed evidence-only; normal VCO task plus B3 conformance carry the useful semantics | Exposes EVAS/Spectre `timer(0)` startup semantics: Spectre has `phase=0.039` at `t=0` while EVAS starts at `0`, but later behavior aligns. | Do not count historical row as bugfix. Ordinary `dut`/`tb`/`e2e` tasks are materialized; startup semantics stay in conformance. |
| `vbm1_voltage_clamp_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source omits the lower clamp while preserving the upper clamp. | EVAS and Spectre confirmed buggy-fail/fixed-pass on 2026-05-15. |

## Immediate Conclusions

- `vbm1_strongarm_comparator_behavior_bugfix` is B1 from original current
  repository evidence. `vbm1_background_calibration_accumulator_bugfix`,
  `vbm1_barrel_pointer_window_bugfix`, `vbm1_cdac_calibration_bugfix`,
  `vbm1_debounce_latch_bugfix`, `vbm1_edge_detector_bugfix`,
  `vbm1_element_shuffler_bugfix`, `vbm1_first_order_lowpass_bugfix`,
  `vbm1_gain_trim_controller_bugfix`, `vbm1_leaky_hold_bugfix`,
  `vbm1_lock_detector_bugfix`, `vbm1_offset_calibration_fsm_bugfix`,
  `vbm1_offset_comparator_bugfix`, `vbm1_one_shot_timer_bugfix`,
  `vbm1_peak_detector_bugfix`, `vbm1_pfd_reset_race_bugfix`,
  `vbm1_precision_rectifier_bugfix`, `vbm1_resettable_integrator_bugfix`,
  `vbm1_rotating_element_selector_bugfix`, `vbm1_sar_logic_4b_bugfix`,
  `vbm1_segmented_dac_bugfix`, `vbm1_slew_rate_limiter_bugfix`,
  `vbm1_thermometer_dac_bugfix`,
  `vbm1_thermometer_decoder_guarded_bugfix`, `vbm1_voltage_clamp_bugfix`
  are now B1-reconstructed cases.
  `vbm1_track_hold_aperture_bugfix` is also B1-reconstructed, with its
  aperture-boundary semantics kept distinct from the functional badcase.
  The D004 confirmed calibration cases (`barrel_pointer_window`,
  `cdac_calibration`) were confirmed with buggy-fail/fixed-pass EVAS and
  Spectre evidence on 2026-05-15. The D004 batch2 calibration cases
  (`element_shuffler`,
  `rotating_element_selector`) and D004 batch3 cases
  (`background_calibration_accumulator`, `debounce_latch`,
  `thermometer_dac`, `thermometer_decoder_guarded`) were confirmed with
  buggy-fail/fixed-pass EVAS and Spectre evidence on 2026-05-14.
  The P2 functional reconstructions (`leaky_hold`, `one_shot_timer`,
  `track_hold_aperture`) were confirmed with buggy-fail/fixed-pass EVAS and
  Spectre evidence on 2026-05-15.
- The D004 B1 expansion batch (`voltage_clamp`, `precision_rectifier`,
  `peak_detector`, `slew_rate_limiter`, `first_order_lowpass`,
  `resettable_integrator`, `gain_trim_controller`, `offset_comparator`,
  `lock_detector`, `offset_calibration_fsm`, and `sar_logic_4b`) was confirmed
  with fixed-pass/buggy-fail EVAS and Spectre evidence on 2026-05-15.
- EVAS/Spectre semantic cases belong in the separate conformance suite. The
  first B3 assets cover `vco_phase_integrator`, file-output timing, and
  settling/done boundary behavior under `conformance/evas-spectre/`.
- Manual review on 2026-05-15 closed the remaining fixed-only bugfix rows as
  evidence-only. `file_metric_writer`, `resettable_counter_divider`,
  `settling_time_measurement_tb`, and `vco_phase_integrator` have staged source
  files identical to their `_dut` rows, so they are not release-facing bugfix
  tasks. Their useful behavior coverage is now represented by ordinary
  `dut`/`tb`/`e2e` tasks and, where appropriate, conformance assets.

## Remaining Fixed-Only Buckets

This bucketization is the next execution queue after the already confirmed B1
rows above. A row can move only after the relevant evidence gate is satisfied.

| Bucket | Rows | Next action | Release-count rule |
| --- | --- | --- | --- |
| B1 reconstructable | None currently queued from the reviewed fixed-only set. | Continue only when a reviewer identifies another realistic single-root-cause defect. | Count as `true-bugfix` only after the dual evidence is present. |
| B2 normal behavior | None remaining from the fixed-only historical bugfix set. | Ordinary `dut`/`tb`/`e2e` tasks are now materialized for `file_metric_writer`, `settling_time_measurement_tb`, and `vco_phase_integrator`. | Count normal behavior only under those non-bugfix task IDs, never under the historical bugfix rows. |
| B3 conformance | File I/O write timing from `vbm1_file_metric_writer_bugfix`; settling/done threshold boundary from `vbm1_settling_time_measurement_tb_bugfix`; `timer(0)` startup and phase accepted-point behavior from `vbm1_vco_phase_integrator_bugfix`; any future B1 candidate whose intended failure is simulator scheduling rather than DUT repair. | Minimal `conformance/evas-spectre/` assets exist for these three axes; next work is a dedicated conformance runner hook. | Exclude from vaBench model-capability and bugfix denominators. |
| B4 evidence-only | `vbm1_background_calibration_accumulator_bugfix`, `vbm1_file_metric_writer_bugfix`, `vbm1_resettable_counter_divider_bugfix`, `vbm1_settling_time_measurement_tb_bugfix`, `vbm1_vco_phase_integrator_bugfix` | Keep validation evidence but block public bugfix release. Reopen only for a new, reviewed single-root-cause badcase or a deliberately separate conformance task. | Exclude from model-capability and bugfix denominators until reclassified. |
