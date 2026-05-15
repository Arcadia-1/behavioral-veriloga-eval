# D004 Bugfix Release Triage

Date: 2026-05-14

This table supports D004 in `VABENCH_SEMANTIC_DECISIONS.md`: historical
`bugfix` rows without current badcases should first be reviewed for a
reconstructable buggy source. A row remains release-facing `bugfix` only after
the reconstructed badcase fails and the fixed source passes the public checker.

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
| `vbm1_file_metric_writer_bugfix` | fixed DUT + TB plus output artifact | B3 conformance preferred; normal measurement task allowed | Uses `$fopen/$fwrite` and a file artifact; current pass evidence mainly proves file/event/tool behavior plus `done` flag. | Do not count historical row as bugfix. Reuse function as `tb-generation`/measurement only when file-output semantics are public; keep atomic file I/O in conformance. |
| `vbm1_first_order_lowpass_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Normal continuous response task; plausible defects include wrong time constant or final target. | Keep tolerances broad enough to avoid solver-grid overfitting. |
| `vbm1_gain_trim_controller_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Calibration/control behavior has plausible sign, clamp, and reset badcases. | Recoverable sign/clamp badcase? |
| `vbm1_leaky_hold_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Buggy source omits the leakage decay multiply, so held output stays high until reset. This is separate from atomic `$abstime` decay conformance. | EVAS and Spectre confirmed fixed-pass/buggy-fail on 2026-05-15. |
| `vbm1_lock_detector_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Lock assertion behavior has plausible streak-counter or tolerance defects. | Use time-weighted lock duration/edge time as release metric. |
| `vbm1_offset_calibration_fsm_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Normal calibration FSM; wrong-direction or missing saturation bugs are plausible. | Any historical wrong-direction update badcase? |
| `vbm1_offset_comparator_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Comparator offset polarity/threshold mistakes are plausible repair defects. | If no badcase is reconstructed, publish as comparator behavior only. |
| `vbm1_one_shot_timer_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + reset-during-pulse TB | B1-reconstructed | Buggy source omits the falling reset handler, so an active pulse waits for the timer instead of clearing immediately. | EVAS and Spectre confirmed fixed-pass/buggy-fail on 2026-05-15. |
| `vbm1_peak_detector_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Peak-hold reset/update bugs are plausible single-cause defects. | Any recoverable reset/hold badcase? |
| `vbm1_pfd_reset_race_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | The DIV edge path forgets to clear both states when UP is already asserted; this creates a persistent UP/DN overlap. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-pilot-*2026-05-14`; EVAS needs a 300s timeout budget for this dense 10ps-step case. |
| `vbm1_precision_rectifier_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Polarity/dead-zone defects are plausible. | Publish as behavior-regression only if no realistic badcase is found. |
| `vbm1_resettable_counter_divider_bugfix` | two reference-like DUTs + TB | B1-review | Has `clk_divider.va` and `clk_divider_ref.va`, but neither is clearly labeled buggy/fixed. | Determine whether one file is actually a badcase or just alternate specs. |
| `vbm1_resettable_integrator_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Reset, integration sign, or accumulation bugs are plausible. | Add conformance only if reset/sample ordering diverges. |
| `vbm1_rotating_element_selector_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Off-by-one wrap at `idx >= 3` skips selector state 3, producing `1,2,0,1,2,0` instead of `1,2,3,0,1,2`. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-batch2-*2026-05-14`. |
| `vbm1_sar_logic_4b_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | SAR bit-cycling and decision update bugs are plausible. | Choose one realistic SAR state/update defect. |
| `vbm1_segmented_dac_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | The thermometer segment is weighted as two binary LSBs instead of four, compressing upper-code output levels. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-pilot-*2026-05-14`. |
| `vbm1_settling_time_measurement_tb_bugfix` | fixed DUT/TB measurement only | B3 measurement/conformance preferred; normal `tb`/`e2e` task allowed | Timer-driven first-order response and `done` threshold are measurement/testbench semantics rather than a DUT repair pair. | Do not count historical row as bugfix. Reuse as `tb-generation` or `e2e` settling-measurement coverage if prompt/checker are reviewed. |
| `vbm1_slew_rate_limiter_bugfix` | fixed DUT + TB only | B1-reconstruct, B2 fallback | Clamp/slope/update bugs are plausible. | Any recoverable clamp/slope bug? |
| `vbm1_strongarm_comparator_behavior_bugfix` | `dut_buggy.va` + `dut_fixed.va` + TB | B1 | Explicit buggy/fixed pair; reset-priority defect is visible in source. | Keep as release-facing bugfix. |
| `vbm1_thermometer_dac_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed with semantic rename | Historical id says thermometer DAC, but the source is a 4-bit binary DAC. Endpoint scaling divides by 16 instead of 15, so full-scale code 15 never reaches `vref`. | Keep historical `task_id` for main120 traceability, but present/release this as a 4-bit binary DAC task. Add a separate true 15-segment thermometer DAC task later. |
| `vbm1_thermometer_decoder_guarded_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + TB | B1-reconstructed | Binary code is decoded as one-hot rather than cumulative thermometer outputs. | EVAS and Spectre confirmed buggy-fail/fixed-pass in `results/d004-batch3-*2026-05-14`. |
| `vbm1_track_hold_aperture_bugfix` | reconstructed `dut_buggy.va` + `dut_fixed.va` + aperture-discriminating TB | B1-reconstructed | Buggy source samples at the clock edge instead of at `clk+taperture`; the TB moves `vin` between those times and checks a later safe window. | EVAS and Spectre confirmed fixed-pass/buggy-fail on 2026-05-15. |
| `vbm1_vco_phase_integrator_bugfix` | fixed DUT + TB only | B3 conformance preferred for startup; normal VCO task allowed | Exposes EVAS/Spectre `timer(0)` startup semantics: Spectre has `phase=0.039` at `t=0` while EVAS starts at `0`, but later behavior aligns. | Do not count historical row as bugfix. Reuse VCO as `spec-to-va`/`e2e` with safe post-startup metrics; keep startup semantic in conformance. |
| `vbm1_voltage_clamp_bugfix` | generic fixed DUT + TB only | B1-reconstruct, B2 fallback | Clamp bound, source polarity, or transition bugs are plausible. | Need prompt review because source names are generic. |

## Immediate Conclusions

- `vbm1_strongarm_comparator_behavior_bugfix` is B1 from original current
  repository evidence. `vbm1_background_calibration_accumulator_bugfix`,
  `vbm1_barrel_pointer_window_bugfix`, `vbm1_cdac_calibration_bugfix`,
  `vbm1_debounce_latch_bugfix`, `vbm1_edge_detector_bugfix`,
  `vbm1_element_shuffler_bugfix`, `vbm1_leaky_hold_bugfix`,
  `vbm1_one_shot_timer_bugfix`, `vbm1_pfd_reset_race_bugfix`,
  `vbm1_rotating_element_selector_bugfix`, `vbm1_segmented_dac_bugfix`,
  `vbm1_thermometer_dac_bugfix`,
  `vbm1_thermometer_decoder_guarded_bugfix` are now B1-reconstructed cases.
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
- Most fixed-only rows are now B1 reconstruction candidates, not immediate B2
  behavior-regression tasks. They become public `bugfix` only after a realistic
  reconstructed `dut_buggy.va` fails and the fixed source passes.
- EVAS/Spectre semantic cases belong in the separate conformance suite. The
  strongest current B3 candidates are `vco_phase_integrator`, file/final-step
  measurement rows, and any timer/decay case whose intended failure is simulator
  scheduling rather than a model repair defect.
- `resettable_counter_divider` needs manual review before classification,
  because it contains two Verilog-A sources but the file names do not prove a
  buggy/fixed pair.

## Remaining Fixed-Only Buckets

This bucketization is the next execution queue after the already confirmed B1
rows above. A row can move only after the relevant evidence gate is satisfied.

| Bucket | Rows | Next action | Release-count rule |
| --- | --- | --- | --- |
| B1 reconstructable | `vbm1_first_order_lowpass_bugfix`, `vbm1_gain_trim_controller_bugfix`, `vbm1_lock_detector_bugfix`, `vbm1_offset_calibration_fsm_bugfix`, `vbm1_offset_comparator_bugfix`, `vbm1_peak_detector_bugfix`, `vbm1_precision_rectifier_bugfix`, `vbm1_resettable_integrator_bugfix`, `vbm1_sar_logic_4b_bugfix`, `vbm1_slew_rate_limiter_bugfix`, `vbm1_voltage_clamp_bugfix` | Design one realistic single-root-cause `dut_buggy.va`, keep fixed gold as `dut_fixed.va`, and require EVAS/Spectre buggy-fail plus fixed-pass. | Count as `true-bugfix` only after the dual evidence is present. |
| B2 normal behavior | `vbm1_file_metric_writer_bugfix`, `vbm1_settling_time_measurement_tb_bugfix`, `vbm1_vco_phase_integrator_bugfix` | Reframe as non-bugfix `tb-generation`, `spec-to-va`, or `end-to-end` tasks with public behavior prompts after extracting atomic simulator semantics into conformance. | Count as model capability only under the new non-bugfix family, never as bugfix claim. |
| B3 conformance | File I/O write timing from `vbm1_file_metric_writer_bugfix`; settling/done threshold boundary from `vbm1_settling_time_measurement_tb_bugfix`; `timer(0)` startup and phase accepted-point behavior from `vbm1_vco_phase_integrator_bugfix`; any future B1 candidate whose intended failure is simulator scheduling rather than DUT repair. | Create minimal `conformance/evas-spectre/` assets, each with exactly one semantic axis and explicit EVAS/Spectre expected relation. | Exclude from vaBench model-capability and bugfix denominators. |
| B4 evidence-only | `vbm1_background_calibration_accumulator_bugfix`, `vbm1_resettable_counter_divider_bugfix` | Keep validation evidence but block public release until a distinct defect is designed (`background_calibration_accumulator`) or the two-source fixture is manually identified as a real buggy/fixed pair (`resettable_counter_divider`). | Exclude from model-capability and bugfix denominators until reclassified. |
