#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


EVAS_DIR = Path("results/vabench-main-v1-main120-gold-evas-2026-05-08")
SPECTRE_DIR = Path("results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08")
INVENTORY_CSV = Path("docs/VABENCH_MAIN120_MATERIALIZATION.csv")
REVIEW_DOC = Path("docs/VABENCH_MAIN120_NORMAL_MATERIALIZATION_BATCH.md")

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "e2e": "end-to-end",
}

FAMILY_TO_ROOT = {
    "spec-to-va": Path("tasks/spec-to-va/voltage"),
    "tb-generation": Path("tasks/tb-generation/voltage"),
    "end-to-end": Path("tasks/end-to-end/voltage"),
}

DEFAULT_MUST_NOT = ["I(", "ddt(", "idt("]


@dataclass(frozen=True)
class BaseSpec:
    category: str
    difficulty: str
    title: str
    module: str
    ports: str
    primary_va: str
    tb_file: str
    behavior: list[str]
    stimulus: list[str]
    checks: list[str]
    syntax: list[str]
    tolerance_notes: str
    public_caveat: str = ""
    semantic_risk: str = ""
    release_decision: str = ""
    checker_boundary: str = ""


CLEAN_TASK_IDS = {
    "vbm1_thermometer_dac_dut": "vbm1_simple_binary_voltage_dac_4b_dut",
    "vbm1_thermometer_dac_tb": "vbm1_simple_binary_voltage_dac_4b_tb",
    "vbm1_thermometer_dac_e2e": "vbm1_simple_binary_voltage_dac_4b_e2e",
}


BASE_SPECS: dict[str, BaseSpec] = {
    "background_calibration_accumulator": BaseSpec(
        category="calibration",
        difficulty="easy",
        title="background calibration accumulator",
        module="background_calibration_accumulator",
        ports="clk, rst, err, accum",
        primary_va="background_calibration_accumulator.va",
        tb_file="tb_background_calibration_accumulator_ref.scs",
        behavior=[
            "Initialize `accum` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.",
            "When reset is low, add 0.04 V on each rising `clk` edge if `err` is high, otherwise subtract 0.04 V.",
            "Clamp the accumulator to the inclusive range 0.05 V to 0.85 V and drive `accum` with `transition()`.",
        ],
        stimulus=[
            "Use a 0/0.9 V clock with 20 ns period and a reset that releases near 16 ns.",
            "Drive `err` high, then low, then high again so the checker sees increment, decrement, and recovery windows.",
            "Run transient analysis to 220 ns with saved `clk`, `rst`, `err`, and `accum`.",
        ],
        checks=[
            "reset_sample_near_0p45",
            "accum_increments_then_decrements_then_recovers",
            "accum_clamped_to_0p05_0p85",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Use fixed safe-time samples after clock edges; ignore final raw row value.",
    ),
    "cdac_calibration": BaseSpec(
        category="dac",
        difficulty="easy",
        title="trim-voltage generator",
        module="cdac_calibration",
        ports="clk, rst, err, trim",
        primary_va="cdac_calibration.va",
        tb_file="tb_cdac_calibration_ref.scs",
        behavior=[
            "Implement a voltage-domain calibration accumulator that generates a trim voltage, not a capacitor-array CDAC model.",
            "Initialize `trim` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.",
            "When reset is low, add 0.06 V on high `err`, subtract 0.06 V on low `err`, clamp to 0.05 V to 0.85 V, and drive through `transition()`.",
        ],
        stimulus=[
            "Use a 20 ns period clock, reset release near 16 ns, and an `err` waveform that is high, low, then high.",
            "Run to 220 ns with 500 ps maxstep and save `clk`, `rst`, `err`, and `trim`.",
        ],
        checks=[
            "reset_trim_near_0p45",
            "trim_increments_decrements_and_recovers",
            "trim_clamped_to_0p05_0p85",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="This task is semantically a trim-voltage generator; do not compare against a full CDAC transfer curve.",
        public_caveat="Historical naming can suggest a full capacitor-array CDAC; this public task is only the voltage-domain calibration accumulator that drives `trim`.",
        semantic_risk="Historical CDAC wording can be misread as a full capacitor-array DAC transfer-model task.",
        release_decision="Release as a trim-voltage generator task, not as a full CDAC model.",
        checker_boundary="Check reset, increment/decrement, and clamp windows; do not score a capacitor-array transfer curve.",
    ),
    "debounce_latch": BaseSpec(
        category="digital-logic",
        difficulty="medium",
        title="debounced latch with delayed qualification",
        module="debounce_latch",
        ports="sig, rst_n, out",
        primary_va="debounce_latch.va",
        tb_file="tb_debounce_latch_ref.scs",
        behavior=[
            "Use active-low reset `rst_n`; reset forces `out` low and cancels any pending qualification.",
            "On a rising `sig` edge while reset is released, arm a 12 ns qualification timer.",
            "On the timer event, set `out` high only if `sig` and `rst_n` are still high; falling `sig` clears or cancels the output.",
        ],
        stimulus=[
            "Create short rejected pulses and longer accepted pulses on `sig` after reset releases.",
            "Run long enough to observe at least one rejected pulse and one qualified high output.",
            "Save `sig`, `rst_n`, and `out`.",
        ],
        checks=[
            "short_glitch_rejected",
            "stable_high_qualified_after_delay",
            "falling_sig_clears_output",
        ],
        syntax=["@(cross(", "@(timer(", "transition("],
        tolerance_notes="Check post-timer stable windows rather than the exact timer row.",
    ),
    "file_metric_writer": BaseSpec(
        category="measurement",
        difficulty="medium",
        title="file metric writer",
        module="file_metric_writer",
        ports="vin, done",
        primary_va="file_metric_writer.va",
        tb_file="tb_file_metric_writer_ref.scs",
        behavior=[
            "Open a text metric file at startup using a string parameter named `filename` with default `metric.out`.",
            "On the first rising crossing of `vin` through 0.45 V, write the crossing time to the metric file and set `done` high.",
            "Keep `done` low before the first crossing and high afterwards; drive it with smoothed voltage transitions.",
        ],
        stimulus=[
            "Drive `vin` through exactly one public rising crossing near 30 ns.",
            "Run to a later safe window and save `vin` and `done`; the file side effect is supporting evidence, not the only metric.",
        ],
        checks=[
            "done_low_before_crossing",
            "done_high_after_first_crossing",
            "metric_file_records_first_crossing_time",
        ],
        syntax=["@(initial_step", "@(cross(", "$fopen", "$fwrite", "transition("],
        tolerance_notes="Waveform checks are primary; file contents are checked as bounded side-effect evidence.",
        public_caveat="This is a normal measurement/file-output task. It is not a bugfix task; atomic file I/O semantics belong in EVAS/Spectre conformance.",
        semantic_risk="File I/O can be mistaken for repair evidence or for a broad simulator capability claim.",
        release_decision="Release as normal measurement behavior only; keep file-output timing as conformance coverage.",
        checker_boundary="Validate `done` waveform and first-crossing file content without counting the historical bugfix row.",
    ),
    "first_order_lowpass": BaseSpec(
        category="amplifier-filter",
        difficulty="easy",
        title="timer-discretized first-order lowpass",
        module="first_order_lowpass",
        ports="vin, vout",
        primary_va="first_order_lowpass.va",
        tb_file="tb_first_order_lowpass_ref.scs",
        behavior=[
            "Use a 500 ps timer update with state `y += 0.025 * (V(vin) - y)`.",
            "Drive `vout` from the internal state with `transition()`.",
            "The response must be monotone and visibly slower than an instantaneous copy.",
        ],
        stimulus=[
            "Apply a 0 to high step on `vin` and run long enough for the lowpass output to settle.",
            "Save `vin` and `vout` for fixed-time response checks.",
        ],
        checks=[
            "vout_monotone_step_response",
            "vout_not_instantaneous",
            "vout_reaches_expected_late_level",
        ],
        syntax=["@(timer(", "transition("],
        tolerance_notes="Use safe-time level windows to avoid judging the exact discrete update row.",
    ),
    "gain_trim_controller": BaseSpec(
        category="calibration",
        difficulty="medium",
        title="gain trim controller",
        module="gain_trim_controller",
        ports="clk, rst, meas, target, gain_ctrl",
        primary_va="gain_trim_controller.va",
        tb_file="tb_gain_trim_controller_ref.scs",
        behavior=[
            "Initialize and reset `gain_ctrl` to 0.30 V on rising `clk` while `rst` is high.",
            "When `meas` is below `target - 0.02`, increase the control by 0.05 V; when above `target + 0.02`, decrease it by 0.05 V.",
            "Hold inside the deadband, clamp to 0.05 V to 0.85 V, and drive through `transition()`.",
        ],
        stimulus=[
            "Provide target and measured waveforms that create low-measured and high-measured windows long enough to hit both clamps.",
            "Run transient analysis with clocked samples through trim increase, upper clamp, trim decrease, and lower clamp phases.",
        ],
        checks=[
            "reset_gain_control_near_0p30",
            "low_measured_value_increases_control",
            "high_measured_value_decreases_control",
            "gain_control_reaches_high_and_low_clamps",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Use clock-edge settled samples; do not inspect the final simulator row.",
    ),
    "leaky_hold": BaseSpec(
        category="sample-hold",
        difficulty="medium",
        title="leaky sample-and-hold",
        module="leaky_hold",
        ports="sample, rst, vout",
        primary_va="leaky_hold.va",
        tb_file="tb_leaky_hold_ref.scs",
        behavior=[
            "A rising `sample` edge captures a fixed 0.75 V held level.",
            "A 1 ns timer applies exponential droop by multiplying the held value by 0.985 while reset is low.",
            "High `rst` clears the held value; drive `vout` through `transition()`.",
        ],
        stimulus=[
            "Generate capture events, an observable droop interval, reset clearing, and a second capture.",
            "Save `sample`, `rst`, and `vout`.",
        ],
        checks=[
            "capture_reaches_high_level",
            "held_output_droops_over_time",
            "reset_clears_output",
            "second_capture_recovers",
        ],
        syntax=["@(cross(", "@(timer(", "transition("],
        tolerance_notes="Check droop across wide windows, not a single exact timer tick.",
    ),
    "lock_detector": BaseSpec(
        category="pll-clock",
        difficulty="medium",
        title="reference-feedback lock detector",
        module="lock_detector",
        ports="ref_clk, fb_clk, rst_n, lock",
        primary_va="lock_detector.va",
        tb_file="tb_lock_detector_ref.scs",
        behavior=[
            "Use active-low reset to clear lock state and the consecutive-hit counter.",
            "Record rising feedback-clock edge times and compare them against rising reference-clock edges.",
            "Assert `lock` after three consecutive reference events whose feedback edge is within 2 ns.",
        ],
        stimulus=[
            "Drive initial mismatched or unsettled clocks followed by aligned reference and feedback clocks.",
            "Save `ref_clk`, `fb_clk`, `rst_n`, and `lock`.",
        ],
        checks=[
            "lock_low_before_three_good_edges",
            "lock_high_after_consecutive_aligned_edges",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Use reference-cycle windows; do not require exact analog event ordering at coincident rows.",
    ),
    "offset_calibration_fsm": BaseSpec(
        category="calibration",
        difficulty="medium",
        title="offset calibration FSM",
        module="offset_calibration_fsm",
        ports="clk, rst, comp, trim",
        primary_va="offset_calibration_fsm.va",
        tb_file="tb_offset_calibration_fsm_ref.scs",
        behavior=[
            "Initialize and reset `trim` to 0.45 V on rising `clk` with `rst` high.",
            "On each rising clock after reset, add 0.08 V when `comp` is high and subtract 0.08 V when `comp` is low.",
            "Clamp `trim` to 0.05 V to 0.85 V and drive through `transition()`.",
        ],
        stimulus=[
            "Drive comparator decisions high, then low, then high so the trim increases, decreases, and recovers.",
            "Save `clk`, `rst`, `comp`, and `trim`.",
        ],
        checks=[
            "trim_increases_on_high_comparator",
            "trim_decreases_on_low_comparator",
            "trim_recovers_on_late_high_comparator",
            "trim_clamped",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Use fixed post-clock sample windows.",
    ),
    "offset_comparator": BaseSpec(
        category="comparator",
        difficulty="easy",
        title="clocked comparator with input offset",
        module="cmp_offset_ref",
        ports="VDD, VSS, CLK, VINP, VINN, OUT_P",
        primary_va="cmp_offset_ref.va",
        tb_file="tb_comparator_offset_ref.scs",
        behavior=[
            "On each rising `CLK` edge, compare `VINP - VINN` against an internal positive offset threshold.",
            "Drive `OUT_P` to the supply level for a high decision and to `VSS` for a low decision.",
            "Use smoothed voltage-domain output transitions.",
        ],
        stimulus=[
            "Sweep `VINP` around `VINN` while clocking the comparator.",
            "Save the clock, differential inputs, and output so low/high/low decisions are visible.",
        ],
        checks=[
            "clocked_output_sequence_LHHHLLL",
            "offset_threshold_affects_borderline_decisions",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Judge settled post-clock decisions, not continuous-time comparator behavior.",
    ),
    "one_shot_timer": BaseSpec(
        category="analog-events",
        difficulty="medium",
        title="one-shot pulse timer",
        module="one_shot_timer",
        ports="trig, rst_n, pulse",
        primary_va="one_shot_timer.va",
        tb_file="tb_one_shot_timer_ref.scs",
        behavior=[
            "Use active-low reset to clear any active or pending pulse.",
            "On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.",
            "The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.",
        ],
        stimulus=[
            "Drive multiple trigger events with reset released and include windows before, during, and after each pulse.",
            "Save `trig`, `rst_n`, and `pulse`.",
        ],
        checks=[
            "pulse_goes_high_after_trigger",
            "pulse_width_about_8ns",
            "reset_keeps_pulse_low",
        ],
        syntax=["@(cross(", "@(timer(", "transition("],
        tolerance_notes="Use pulse windows with tolerance around the programmed 8 ns width.",
    ),
    "peak_detector": BaseSpec(
        category="measurement",
        difficulty="easy",
        title="resettable peak detector",
        module="peak_detector",
        ports="vin, rst, vout",
        primary_va="peak_detector.va",
        tb_file="tb_peak_detector_ref.scs",
        behavior=[
            "Track the maximum observed `vin` value using a timer-sampled internal peak.",
            "High `rst` clears the peak to 0 V.",
            "Drive `vout` from the peak value through `transition()`.",
        ],
        stimulus=[
            "Apply a first input peak, reset clear, and a second larger peak.",
            "Save `vin`, `rst`, and `vout`.",
        ],
        checks=[
            "first_peak_is_held",
            "reset_clears_peak",
            "second_peak_updates_to_larger_value",
        ],
        syntax=["@(timer(", "transition("],
        tolerance_notes="Use broad windows around peaks; do not depend on exact timer alignment.",
    ),
    "pfd_reset_race": BaseSpec(
        category="phase-detector",
        difficulty="hard",
        title="PFD reset-race UP/DN generator",
        module="pfd_updn",
        ports="VDD, VSS, REF, DIV, UP, DN",
        primary_va="pfd_updn.va",
        tb_file="tb_pfd_reset_race_ref.scs",
        behavior=[
            "Set `UP` high on a rising `REF` edge and set `DN` high on a rising `DIV` edge.",
            "If the opposite output is already high when an edge arrives, clear both outputs to model the reset-race behavior.",
            "Drive `UP` and `DN` as smoothed voltage-domain logic levels.",
        ],
        stimulus=[
            "Use close REF/DIV edge timing and a small maxstep so reset-race ordering is observable.",
            "Save `REF`, `DIV`, `UP`, and `DN`.",
        ],
        checks=[
            "up_and_dn_pulses_exist",
            "overlap_window_is_bounded",
            "outputs_clear_after_race",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Bound overlap and pulse windows instead of requiring a single raw event ordering.",
    ),
    "precision_rectifier": BaseSpec(
        category="amplifier-filter",
        difficulty="easy",
        title="ideal precision rectifier",
        module="precision_rectifier",
        ports="vin, vout",
        primary_va="precision_rectifier.va",
        tb_file="tb_precision_rectifier_ref.scs",
        behavior=[
            "Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.",
            "Use only voltage-domain contributions and smooth the output with `transition()`.",
        ],
        stimulus=[
            "Apply negative, near-zero, and positive input intervals.",
            "Save `vin` and `vout` for rectification checks.",
        ],
        checks=[
            "negative_input_rectifies_to_zero",
            "positive_input_follows_input",
            "near_zero_has_no_large_offset",
        ],
        syntax=["transition("],
        tolerance_notes="Check level windows away from zero crossings.",
    ),
    "resettable_counter_divider": BaseSpec(
        category="digital-logic",
        difficulty="medium",
        title="resettable programmable clock divider",
        module="clk_divider_ref",
        ports=(
            "clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, "
            "div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock"
        ),
        primary_va="clk_divider_ref.va",
        tb_file="tb_clk_divider_ref.scs",
        behavior=[
            "Decode an 8-bit voltage-domain ratio code into an integer divide ratio, with code 0 treated as ratio 1.",
            "Use active-low reset to clear the counter, output state, and lock state.",
            "For ratio greater than 1, divide the input clock with floor/ceil high and low segment lengths; assert `lock` after the first complete output period.",
        ],
        stimulus=[
            "Drive `div_code` to ratio 5, release reset near 2 ns, and clock with a 1 ns input period.",
            "Run to 80 ns with a small maxstep and save input clock, output clock, lock, reset, and all ratio bits.",
        ],
        checks=[
            "ratio_code_decodes_to_5",
            "output_period_matches_five_input_edges",
            "lock_asserts_after_first_complete_output_period",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Measure edge intervals after startup; ignore the legacy auxiliary `clk_divider.va` file.",
        public_caveat="The staged evidence also preserves an auxiliary legacy `clk_divider.va`; the public task contract targets `clk_divider_ref`.",
        semantic_risk="The staged directory contains a legacy auxiliary source that is not instantiated by the public testbench.",
        release_decision="Release the normal divider task against `clk_divider_ref`; do not treat legacy `clk_divider.va` as a badcase.",
        checker_boundary="Measure divider ratio, output period, and lock after startup; ignore the unused auxiliary source.",
    ),
    "resettable_integrator": BaseSpec(
        category="amplifier-filter",
        difficulty="medium",
        title="resettable timer integrator",
        module="resettable_integrator",
        ports="vin, rst, vout",
        primary_va="resettable_integrator.va",
        tb_file="tb_resettable_integrator_ref.scs",
        behavior=[
            "Use a 1 ns timer update to integrate `vin` into an internal accumulator.",
            "High `rst` clears the accumulator to 0 V.",
            "Clamp the accumulator between 0 V and 0.85 V and drive `vout` with `transition()`.",
        ],
        stimulus=[
            "Drive a positive input, reset pulse, and post-reset positive input interval.",
            "Save `vin`, `rst`, and `vout` across pre-reset integration, reset clearing, and restart windows.",
        ],
        checks=[
            "pre_reset_output_integrates_up",
            "reset_clears_integrator",
            "post_reset_integration_restarts",
        ],
        syntax=["@(timer(", "transition("],
        tolerance_notes="Use post-reset safe windows rather than exact reset-edge samples.",
    ),
    "sar_logic_4b": BaseSpec(
        category="adc-sar",
        difficulty="medium",
        title="4-bit SAR logic sequencer",
        module="sar_logic_4b",
        ports="VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY",
        primary_va="sar_logic_4b.va",
        tb_file="tb_sar_logic_4b_ref.scs",
        behavior=[
            "Implement a 4-bit successive-approximation state machine clocked by rising `CLKS` edges.",
            "Resolve the current trial bit from `DCOMP`, advance to the next lower bit, and assert `RDY` after bit 0 is resolved.",
            "Drive DAC decision pins and `RDY` as 0/0.9 V voltage-domain outputs with `transition()`.",
        ],
        stimulus=[
            "Clock the SAR through repeated conversion cycles with comparator decisions that produce code 1010 at the checked window.",
            "Save `CLKS`, `DCOMP`, all DAC decision pins, and `RDY`.",
        ],
        checks=[
            "rdy_low_high_low_sequence",
            "dac_code_1010_at_conversion_done_window",
        ],
        syntax=["@(cross(", "transition("],
        tolerance_notes="Judge state at conversion windows, not transient trial-bit rows.",
    ),
    "settling_time_measurement_tb": BaseSpec(
        category="measurement",
        difficulty="medium",
        title="settling response measurement helper",
        module="settling_time_measurement_tb",
        ports="step, vout, done",
        primary_va="settling_time_measurement_tb.va",
        tb_file="tb_settling_time_measurement_tb_ref.scs",
        behavior=[
            "Use a 1 ns timer update with `y += 0.04 * (V(step) - y)` to model a settling response.",
            "Drive `vout` from `y`; assert `done` only after 120 ns and once `y` is above 0.75 V.",
            "This is a measurement-helper behavior task, not a true bugfix task.",
        ],
        stimulus=[
            "Apply a step input and run past the 120 ns settling boundary.",
            "Save `step`, `vout`, and `done` with enough samples before and after the boundary.",
        ],
        checks=[
            "vout_rises_monotonically_toward_step",
            "done_low_before_boundary",
            "done_high_in_late_settled_window",
        ],
        syntax=["@(timer(", "transition("],
        tolerance_notes="Use late settled windows after 120 ns; exact boundary semantics live in the conformance set.",
        public_caveat="This is a normal measurement-helper behavior task. It is not a bugfix task; exact 120 ns boundary semantics belong in conformance.",
        semantic_risk="The `done` threshold can be over-interpreted as exact-boundary simulator conformance or repair evidence.",
        release_decision="Release as normal measurement-helper behavior; keep strict boundary behavior in EVAS/Spectre conformance.",
        checker_boundary="Use safe pre-boundary and late settled windows, not the exact 120 ns row.",
    ),
    "slew_rate_limiter": BaseSpec(
        category="signal-source",
        difficulty="easy",
        title="discrete slew-rate limiter",
        module="slew_rate_limiter",
        ports="vin, vout",
        primary_va="slew_rate_limiter.va",
        tb_file="tb_slew_rate_limiter_ref.scs",
        behavior=[
            "Use a 1 ns timer update and move the internal output toward `vin` by at most 0.015 V per update.",
            "Limit both rising and falling changes and drive `vout` with `transition()`.",
        ],
        stimulus=[
            "Apply a large upward step, hold, then a downward step.",
            "Save `vin` and `vout` to verify limited rising and falling slopes and eventual settling.",
        ],
        checks=[
            "rising_slew_is_limited",
            "high_level_eventually_reached",
            "falling_slew_is_limited",
            "low_level_eventually_reached",
        ],
        syntax=["@(timer(", "transition("],
        tolerance_notes="Use level windows; do not require exact per-row step size at transition boundaries.",
    ),
    "thermometer_dac": BaseSpec(
        category="dac",
        difficulty="easy",
        title="simple 4-bit binary-coded DAC",
        module="simple_binary_voltage_dac_4b",
        ports="code_0, code_1, code_2, code_3, vref, vss, aout",
        primary_va="simple_binary_voltage_dac_4b.va",
        tb_file="tb_simple_binary_voltage_dac_4b_ref.scs",
        behavior=[
            "Implement the simple mathematical 4-bit binary-coded DAC described by the input code and references.",
            "Interpret `code_0..code_3` as a binary code with weights 1, 2, 4, and 8.",
            "Drive `aout` linearly between `vss` and `vref` using code/15 and smooth with `transition()`; no unit-element or segmented DAC structure is required.",
        ],
        stimulus=[
            "Apply multiple binary codes spanning low, middle, and full-scale values.",
            "Save all code bits and `aout`.",
        ],
        checks=[
            "binary_code_to_level_mapping",
            "midscale_and_fullscale_levels_match_code_over_15",
        ],
        syntax=["transition("],
        tolerance_notes="Check the mathematical binary code-to-voltage mapping; structural DAC variants live in separate tasks.",
        public_caveat="This is a behavioral binary-weighted transfer model, not a unit-element or segmented DAC implementation.",
    ),
    "thermometer_decoder_guarded": BaseSpec(
        category="dac",
        difficulty="easy",
        title="guarded thermometer decoder",
        module="thermometer_decoder_guarded",
        ports="b0, b1, en, th0, th1, th2, th3",
        primary_va="thermometer_decoder_guarded.va",
        tb_file="tb_thermometer_decoder_guarded_ref.scs",
        behavior=[
            "Decode a 2-bit binary input into cumulative thermometer outputs while `en` is high.",
            "With `en` low, force all thermometer outputs low.",
            "For codes 1, 2, and 3, assert `th0`, then `th0:th1`, then `th0:th2`; `th3` remains guarded low for this 2-bit input space.",
        ],
        stimulus=[
            "Exercise enable-low, code 1, code 2, and code 3 windows.",
            "Save inputs and all thermometer outputs.",
        ],
        checks=[
            "enable_low_forces_all_low",
            "cumulative_sequence_for_codes_1_2_3",
            "guarded_th3_remains_low",
        ],
        syntax=["transition("],
        tolerance_notes="Check fixed code windows rather than transition rows.",
    ),
    "track_hold_aperture": BaseSpec(
        category="sample-hold",
        difficulty="medium",
        title="sample-and-hold with aperture delay",
        module="sample_hold_aperture_ref",
        ports="VDD, VSS, clk, vin, vout",
        primary_va="sample_hold_aperture_ref.va",
        tb_file="tb_sample_hold_aperture_ref.scs",
        behavior=[
            "On a rising `clk` edge, schedule sampling after a 200 ps aperture delay.",
            "At the aperture timer event, capture `vin` and hold it on `vout` until the next sample.",
            "Drive `vout` with smoothed voltage-domain transitions.",
        ],
        stimulus=[
            "Drive a changing input around clock edges so aperture-delayed sampling is distinguishable from immediate sampling.",
            "Save `clk`, `vin`, and `vout`.",
        ],
        checks=[
            "sampled_values_match_aperture_delayed_input",
            "held_output_remains_between_samples",
        ],
        syntax=["@(cross(", "@(timer(", "transition("],
        tolerance_notes="Use post-aperture settled sample windows.",
    ),
    "vco_phase_integrator": BaseSpec(
        category="pll-clock",
        difficulty="medium",
        title="timer-driven VCO phase integrator",
        module="vco_phase_integrator",
        ports="vctrl, phase, clk",
        primary_va="vco_phase_integrator.va",
        tb_file="tb_vco_phase_integrator_ref.scs",
        behavior=[
            "Use a 1 ns timer update and increment phase by `0.03 + 0.09 * V(vctrl)` at each update.",
            "Wrap phase at 1.0 and toggle `clk` on each wrap.",
            "Drive both `phase` and `clk` through `transition()`.",
        ],
        stimulus=[
            "Drive `vctrl` through low and higher-control intervals so the late clock edge rate is faster than the early edge rate.",
            "Save `vctrl`, `phase`, and `clk` across a long transient.",
        ],
        checks=[
            "phase_span_covers_nearly_full_wrap",
            "clock_toggles_on_phase_wrap",
            "late_edge_rate_exceeds_early_edge_rate",
        ],
        syntax=["@(initial_step", "@(timer(", "transition("],
        tolerance_notes="Score phase-span and edge-rate behavior across stable control-voltage intervals.",
    ),
    "voltage_clamp": BaseSpec(
        category="signal-source",
        difficulty="easy",
        title="voltage clamp",
        module="voltage_clamp",
        ports="raw_level, vdd, vss, clamped_level",
        primary_va="dut.va",
        tb_file="tb_ref.scs",
        behavior=[
            "Clamp `raw_level` to the public range 0.18 V to 0.72 V.",
            "Drive `clamped_level` through `transition()` using voltage-domain contributions only.",
        ],
        stimulus=[
            "Drive `raw_level` below range, inside range, and above range.",
            "Save `raw_level`, supplies, and `clamped_level`.",
        ],
        checks=[
            "below_range_clamps_to_0p18",
            "inside_range_follows_raw_level",
            "above_range_clamps_to_0p72",
        ],
        syntax=["transition("],
        tolerance_notes="Check stable level windows away from source transition times.",
    ),
}


def load_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bullet_lines(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def sentence_list(lines: list[str]) -> str:
    return "\n".join(f"- `{line}`" if line.startswith("vbm1_") else f"- {line}" for line in lines)


def render_prompt(task_id: str, form: str, spec: BaseSpec) -> str:
    module_contract = (
        f"The DUT module is `{spec.module}` with ports `{spec.ports}`. "
        "All ports are electrical; digital-control ports use 0/0.9 V logic levels."
    )
    caveat = f"\n\nReview caveat: {spec.public_caveat}" if spec.public_caveat else ""
    if form == "dut":
        return (
            f"# Task: {task_id}\n\n"
            f"Write a pure voltage-domain Verilog-A module for a {spec.title}.\n\n"
            f"{module_contract}\n\n"
            "Required behavior:\n"
            f"{bullet_lines(spec.behavior)}\n\n"
            "Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`."
            f"{caveat}\n\n"
            f"Return exactly one complete Verilog-A file named `{spec.primary_va}`.\n"
        )
    if form == "tb":
        return (
            f"# Task: {task_id}\n\n"
            f"Write a Spectre testbench for a {spec.title} DUT.\n\n"
            f"{module_contract} The candidate DUT file will be available as `{spec.primary_va}`; "
            "include it with `ahdl_include` and instantiate the DUT using the exact module and port names.\n\n"
            "The testbench must exercise:\n"
            f"{bullet_lines(spec.behavior)}\n\n"
            "Stimulus and observability requirements:\n"
            f"{bullet_lines(spec.stimulus)}"
            f"{caveat}\n\n"
            f"Return exactly one Spectre testbench file named `{spec.tb_file}`.\n"
        )
    if form == "e2e":
        return (
            f"# Task: {task_id}\n\n"
            f"Write both the Verilog-A DUT and Spectre testbench for a {spec.title}.\n\n"
            f"{module_contract}\n\n"
            "Required DUT behavior:\n"
            f"{bullet_lines(spec.behavior)}\n\n"
            "Required testbench behavior:\n"
            f"{bullet_lines(spec.stimulus)}\n\n"
            "Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`."
            f"{caveat}\n\n"
            f"Return exactly two files: `{spec.primary_va}` and `{spec.tb_file}`.\n"
        )
    raise ValueError(f"unsupported form={form!r}")


def meta_must_include(form: str, spec: BaseSpec) -> list[str]:
    if form == "tb":
        return ["ahdl_include", "tran", "save"]
    if form == "e2e":
        return sorted(set(spec.syntax + ["ahdl_include", "tran", "save"]))
    return spec.syntax


def meta_must_not_include(form: str) -> list[str]:
    return [] if form == "tb" else DEFAULT_MUST_NOT


def artifacts(form: str, spec: BaseSpec) -> list[str]:
    if form == "dut":
        return [spec.primary_va]
    if form == "tb":
        return [spec.tb_file]
    return [spec.primary_va, spec.tb_file]


def clean_task_id(task_id: str) -> str:
    return CLEAN_TASK_IDS.get(task_id, task_id)


def render_meta(task_id: str, form: str, spec: BaseSpec, source_files: list[str], source_main120_id: str) -> str:
    family = FORM_TO_FAMILY[form]
    meta = {
        "id": task_id,
        "task_id": task_id,
        "asset_type": "vabench_task",
        "benchmark_split": "vabench-main-v1",
        "family": family,
        "category": spec.category,
        "domain": "voltage",
        "difficulty": spec.difficulty,
        "expected_backend": "evas",
        "release_form": "normal",
        "provenance_status": "clean",
        "source_main120_id": source_main120_id,
        "counts": {
            "model_capability": True,
            "benchmark_coverage": True,
            "bugfix_claim": False,
        },
        "must_include": meta_must_include(form, spec),
        "must_not_include": meta_must_not_include(form),
        "inputs": ["prompt.md"],
        "artifacts": artifacts(form, spec),
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
        "source_files": source_files,
        "evidence": {
            "evas_result": f"{EVAS_DIR.as_posix()}/{source_main120_id}/evas_result.json",
            "spectre_result": f"{SPECTRE_DIR.as_posix()}/{source_main120_id}/spectre_result.json",
        },
    }
    if spec.semantic_risk:
        meta["notes"] = (
            f"Semantic review: {spec.release_decision} "
            f"Risk: {spec.semantic_risk} "
            f"Checker boundary: {spec.checker_boundary}"
        )
        meta["semantic_review"] = {
            "risk": spec.semantic_risk,
            "release_decision": spec.release_decision,
            "checker_boundary": spec.checker_boundary,
        }
    return json.dumps(meta, indent=2) + "\n"


def quote_yaml(value: str) -> str:
    return json.dumps(value)


def yaml_list(values: list[str], indent: str = "    ") -> str:
    if not values:
        return f"{indent}[]"
    return "\n".join(f"{indent}- {quote_yaml(value)}" for value in values)


def render_checks(form: str, spec: BaseSpec) -> str:
    must_include = meta_must_include(form, spec)
    must_not = meta_must_not_include(form)
    text = (
        "syntax:\n"
        "  must_include:\n"
        f"{yaml_list(must_include)}\n"
        "  must_not_include:\n"
        f"{yaml_list(must_not)}\n"
        "dut_compile:\n"
        "  backend: \"evas\"\n"
        "tb_compile:\n"
        "  backend: \"evas\"\n"
        "sim_correct:\n"
        "  checks:\n"
        f"{yaml_list(spec.checks)}\n"
        "parity:\n"
        "  required: true\n"
        f"  tolerance_notes: {quote_yaml(spec.tolerance_notes)}\n"
    )
    if spec.semantic_risk:
        text += (
            "semantic_review:\n"
            f"  risk: {quote_yaml(spec.semantic_risk)}\n"
            f"  release_decision: {quote_yaml(spec.release_decision)}\n"
            f"  checker_boundary: {quote_yaml(spec.checker_boundary)}\n"
        )
    return text


def staged_files(task_id: str) -> list[Path]:
    staged_dir = EVAS_DIR / task_id / "staged"
    if not staged_dir.is_dir():
        raise FileNotFoundError(f"missing staged evidence directory: {staged_dir}")
    return sorted(path for path in staged_dir.iterdir() if path.is_file())


def task_destination(task_id: str, form: str, spec: BaseSpec) -> Path:
    family = FORM_TO_FAMILY[form]
    return FAMILY_TO_ROOT[family] / spec.category / task_id


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def materialize_task(row: dict[str, str]) -> Path:
    source_task_id = row["task_id"]
    task_id = clean_task_id(source_task_id)
    base = row["base"]
    form = row["form"]
    spec = BASE_SPECS[base]
    dest = task_destination(task_id, form, spec)
    gold = dest / "gold"
    gold.mkdir(parents=True, exist_ok=True)

    files = staged_files(source_task_id)
    source_files = []
    for src in files:
        dst_name = src.name
        if base == "thermometer_dac":
            if src.suffix == ".va":
                dst_name = spec.primary_va
            elif src.suffix == ".scs":
                dst_name = spec.tb_file
        dst = gold / dst_name
        if base == "thermometer_dac" and src.suffix in {".va", ".scs"}:
            text = src.read_text(encoding="utf-8", errors="ignore")
            text = text.replace("thermometer_dac_4b", "simple_binary_voltage_dac_4b")
            text = text.replace("tb_thermometer_dac_4b", "tb_simple_binary_voltage_dac_4b")
            write_text(dst, text)
        else:
            shutil.copy2(src, dst)
        source_files.append(f"gold/{dst_name}")

    write_text(dest / "prompt.md", render_prompt(task_id, form, spec))
    write_text(dest / "meta.json", render_meta(task_id, form, spec, source_files, source_task_id))
    write_text(dest / "checks.yaml", render_checks(form, spec))
    return dest


def selected_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in rows:
        if row["form"] not in FORM_TO_FAMILY:
            continue
        if row["base"] not in BASE_SPECS:
            continue
        selected.append(row)
    return selected


def render_review_doc(rows: list[dict[str, str]]) -> str:
    grouped: dict[str, list[str]] = {}
    for row in rows:
        grouped.setdefault(row["base"], []).append(row["form"])

    lines = [
        "# Main120 Normal Source-Task Materialization Batch",
        "",
        "This batch materializes ordinary `dut`, `tb`, and `e2e` rows from validated main120",
        "EVAS/Spectre evidence into release-quality source-controlled benchmark tasks.",
        "",
        "Scope:",
        "",
        "- Include only `release_form=normal` rows with `form in {dut,tb,e2e}`.",
        "- Do not promote remaining fixed-only `bugfix` rows in this pass.",
        "- Copy staged gold files from main120 EVAS evidence and link both EVAS and Spectre result JSONs.",
        "- Review prompt/checker semantics from the public behavior below; staged files are evidence, not the source of the public contract.",
        "",
        "| Base | Forms | Category | Public task contract | Checker intent | Caveat |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for base in sorted(grouped):
        spec = BASE_SPECS[base]
        forms = ", ".join(sorted(grouped[base]))
        behavior = "<br>".join(spec.behavior)
        checks = "<br>".join(f"`{check}`" for check in spec.checks)
        caveat = spec.public_caveat or ""
        lines.append(f"| `{base}` | {forms} | `{spec.category}` | {behavior} | {checks} | {caveat} |")

    reviewed = [base for base in sorted(grouped) if BASE_SPECS[base].semantic_risk]
    lines.extend(
        [
            "",
            "## Release-Readiness Semantic Review",
            "",
            "These rows are release-facing normal tasks, but their names or checks have",
            "known semantic traps. Keep the decision and checker boundary below aligned",
            "with each task `prompt.md`, `meta.json`, and `checks.yaml`.",
            "",
            "| Base | Risk | Decision | Required prompt wording | Checker boundary | Release status |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for base in reviewed:
        spec = BASE_SPECS[base]
        forms = ", ".join(sorted(grouped[base]))
        prompt_wording = spec.public_caveat or spec.release_decision
        lines.append(
            f"| `{base}` | {spec.semantic_risk} | {spec.release_decision} | "
            f"{prompt_wording} | {spec.checker_boundary} | Reviewed for `{forms}` normal tasks. |"
        )

    lines.extend(
        [
            "",
            "Expected inventory after this batch:",
            "",
            "- `has_exact_task_id`: 116/120",
            "- Remaining source-task materialization queue: 0",
            "- Closed evidence-only fixed-only bugfix rows without release tasks: 4",
            "- Main120 simulation evidence remains 120/120 EVAS/Spectre PASS",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default=str(INVENTORY_CSV))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = load_inventory(Path(args.inventory))
    rows_to_materialize = selected_rows(rows)
    if len(rows_to_materialize) != 72:
        raise SystemExit(f"expected 72 ordinary rows to materialize, found {len(rows_to_materialize)}")

    if args.dry_run:
        for row in rows_to_materialize:
            print(row["task_id"])
        return

    written = [materialize_task(row) for row in rows_to_materialize]
    write_text(REVIEW_DOC, render_review_doc(rows_to_materialize))
    print(f"materialized {len(written)} tasks")
    print(f"wrote {REVIEW_DOC}")


if __name__ == "__main__":
    main()
