# DeepSeek v4-pro vaBench Error Cluster Analysis

- Input report: `benchmark-vabench-release-v1/reports/deepseek_full236_latest_after_wrapper_v5_overlay_20260528.json`
- Total rows: 236
- Pass rows: 59
- Failed rows clustered: 177
- Axis counts: {"behavior": 146, "compile": 27, "generation": 4}

## Cluster Summary

| Cluster | Axis | Count | Share | Dominant category | Dominant form | Example |
| --- | --- | ---: | ---: | --- | --- | --- |
| B01 Static transfer/reference/RF/power macro behavior | behavior | 34 | 19.2% | RF and AFE Behavioral Macromodels (18) | e2e (11) | `vbr1_l1_programmable_gain_amplifier:bugfix`: pga_unclamped_range=(-0.000,1.000) |
| B03 State/reset/enable/stuck-output behavior | behavior | 26 | 14.7% | Baseband Signal Conditioning (9) | dut (9) | `vbr1_l1_higher_order_filter:dut`: two_pole_reset_out=0.000 |
| B04 Event/timing/stimulus coverage behavior | behavior | 25 | 14.1% | PLL Clock and Timing Systems (19) | e2e (9) | `vbr1_l1_hysteresis_comparator:e2e`: window_fracs pre=0.377 mid=0.000 post=1.000 |
| B05 Decision/code/quantization sequence behavior | behavior | 24 | 13.6% | Data Converter Models (18) | tb (9) | `vbr1_l1_debounce_latch:tb`: debounce_early_low=LLHH late_high=HH |
| B06 Calibration/DEM/control algorithm behavior | behavior | 20 | 11.3% | Calibration, DEM, and Control (20) | tb (7) | `vbr1_l1_calibration_deadband_controller:dut`: deadband_hold_mismatches=2/10 |
| B02 Dynamic response/filter/baseband behavior | behavior | 9 | 5.1% | Baseband Signal Conditioning (8) | tb (5) | `vbr1_l1_first_order_lowpass:e2e`: lowpass_samples=0.627,0.865,0.982,0.999 input_step=True monotonic=True response_fast_enough=True not_instant=False bo... |
| B07 Sample/hold/aperture/droop behavior | behavior | 8 | 4.5% | Sampling and Analog Memory (8) | tb (4) | `vbr1_l1_acquisition_limited_sample_and_hold:tb`: acq_hold_drifted_after_fall delta=0.316 |
| C01 Verilog-A local/embedded declaration placement | compile | 21 | 11.9% | Data Converter Models (5) | e2e (9) | `vbr1_l1_higher_order_filter:bugfix`: ERROR: Failed to compile Verilog-A file higher_order_filter.va: Parse error at L64:13: Spectre-incompatible local dec... |
| C02 Guarded transition() contribution | compile | 2 | 1.1% | Baseband Signal Conditioning (1) | e2e (1) | `vbr1_l1_soft_hysteretic_limiter:e2e`: ERROR: Failed to compile Verilog-A file soft_hysteretic_limiter.va: Spectre-incompatible Verilog-A: transition() cont... |
| C03 Restricted cross/operator placement | compile | 1 | 0.6% | Comparator and Decision Circuits (1) | e2e (1) | `vbr1_l1_debounce_latch:e2e`: ERROR: Failed to compile Verilog-A file debounce_latch.va: Module debounce_latch uses Spectre-restricted operator(s)... |
| C04 Indexed/vector procedural syntax | compile | 1 | 0.6% | Calibration, DEM, and Control (1) | dut (1) | `vbr1_l1_dwa_dem_encoder:dut`: ERROR: Failed to compile Verilog-A file v2b_4b.va: Parse error at L64:20: Expected ASSIGN, got IDENT ('i') |
| C06 Spectre testbench instance/source syntax | compile | 1 | 0.6% | Data Converter Models (1) | tb (1) | `vbr1_l1_segmented_dac:tb`: ERROR: Failed to parse tb_segmented_dac_ref.scs: Spectre instance/source syntax expects exactly one name before the n... |
| C07 Unsupported event-loop/timer form | compile | 1 | 0.6% | Comparator and Decision Circuits (1) | dut (1) | `vbr1_l1_propagation_delay_comparator:dut`: cmp_delay.va:unsupported_unbounded_event_loop |
| G01 Incomplete generation under fixed output budget | generation | 4 | 2.3% | PLL Clock and Timing Systems (3) | bugfix (2) | `vbr1_l1_bang_bang_phase_detector:bugfix`: generation_status=no_code_extracted finish_reason=length max_tokens=16384 raw_response_length=0 saved_files=0 |

## Interpretation

### B01 Static transfer/reference/RF/power macro behavior

- Count: 34 (19.2% of failures)
- Top categories: RF and AFE Behavioral Macromodels (18), Bias Reference and Power Management (14), Baseband Signal Conditioning (2)
- Top forms: e2e (11), bugfix (9), tb (9), dut (5)
- Interpretation: The candidate compiles but misses an analog static transfer, reference, regulation, or RF/AFE macromodel contract.
- Recommended action: Use checker evidence to inspect whether the prompt underspecified operating points; otherwise count as model circuit-behavior failure.

### B03 State/reset/enable/stuck-output behavior

- Count: 26 (14.7% of failures)
- Top categories: Baseband Signal Conditioning (9), Bias Reference and Power Management (8), Sampling and Analog Memory (5), Comparator and Decision Circuits (3)
- Top forms: dut (9), tb (6), bugfix (6), e2e (5)
- Interpretation: The candidate output is stuck or mishandles reset, enable, hold, release, or lock state.
- Recommended action: Audit prompt state contracts and checker windows; then treat remaining rows as state-machine or initialization failures.

### B04 Event/timing/stimulus coverage behavior

- Count: 25 (14.1% of failures)
- Top categories: PLL Clock and Timing Systems (19), Data Converter Models (3), Comparator and Decision Circuits (2), RF and AFE Behavioral Macromodels (1)
- Top forms: e2e (9), tb (8), bugfix (5), dut (3)
- Interpretation: The generated DUT/TB misses required clocks, edges, pulse windows, phase windows, or stimulus coverage.
- Recommended action: Inspect whether edge counts and timing windows are explicit in public prompts; this cluster is sensitive to prompt observability.

### B05 Decision/code/quantization sequence behavior

- Count: 24 (13.6% of failures)
- Top categories: Data Converter Models (18), Comparator and Decision Circuits (6)
- Top forms: tb (9), e2e (8), dut (4), bugfix (3)
- Interpretation: The generated model produces the wrong comparator decisions, code sequence, DAC/ADC levels, or residue/quantization schedule.
- Recommended action: Use row-level evidence for manual circuit review; these rows usually reflect functional reasoning failures.

### B06 Calibration/DEM/control algorithm behavior

- Count: 20 (11.3% of failures)
- Top categories: Calibration, DEM, and Control (20)
- Top forms: tb (7), e2e (6), bugfix (4), dut (3)
- Interpretation: The generated model misses trim direction, deadband behavior, DEM rotation, calibration search, or controller sequencing.
- Recommended action: These are high-value failures for L2/L1-control claims; inspect whether algorithmic steps are fully specified.

### B02 Dynamic response/filter/baseband behavior

- Count: 9 (5.1% of failures)
- Top categories: Baseband Signal Conditioning (8), RF and AFE Behavioral Macromodels (1)
- Top forms: tb (5), e2e (2), bugfix (1), dut (1)
- Interpretation: The candidate compiles but misses time-domain response shape such as settling, lag, integration, slew limiting, or envelope behavior.
- Recommended action: Check whether the public prompt names required dynamic observables; if yes, this is model dynamic-behavior failure.

### B07 Sample/hold/aperture/droop behavior

- Count: 8 (4.5% of failures)
- Top categories: Sampling and Analog Memory (8)
- Top forms: tb (4), bugfix (2), e2e (2)
- Interpretation: The candidate misses sampling instant, hold value, aperture delay, droop/leakage, or acquisition-window behavior.
- Recommended action: Check prompt timing contracts first; otherwise count as model sampled-analog-memory failure.

### C01 Verilog-A local/embedded declaration placement

- Count: 21 (11.9% of failures)
- Top categories: Data Converter Models (5), Baseband Signal Conditioning (4), PLL Clock and Timing Systems (4), Calibration, DEM, and Control (3)
- Top forms: e2e (9), bugfix (6), dut (6)
- Interpretation: The candidate uses Spectre-incompatible local or embedded declarations inside analog/procedural statements.
- Recommended action: This is a model Verilog-A subset failure; public/wrapper rules already need to discourage this pattern.

### C02 Guarded transition() contribution

- Count: 2 (1.1% of failures)
- Top categories: Baseband Signal Conditioning (1), Calibration, DEM, and Control (1)
- Top forms: e2e (1), bugfix (1)
- Interpretation: The candidate places transition() contributions inside conditional/event/loop/case control.
- Recommended action: This is a model Verilog-A/Spectre subset failure and an EVAS/Spectre compatibility rule to keep explicit.

### C03 Restricted cross/operator placement

- Count: 1 (0.6% of failures)
- Top categories: Comparator and Decision Circuits (1)
- Top forms: e2e (1)
- Interpretation: The candidate uses cross or another restricted analog operator inside conditionally executed code.
- Recommended action: This is a model Verilog-A subset failure; future prompts can keep the operator-placement rule in the wrapper/EVAS rules.

### C04 Indexed/vector procedural syntax

- Count: 1 (0.6% of failures)
- Top categories: Calibration, DEM, and Control (1)
- Top forms: dut (1)
- Interpretation: The candidate emits indexed analog/vector/procedural syntax that the evaluator/Spectre parser rejects.
- Recommended action: Treat as a syntax/subset failure unless a row-specific checker indicates an extraction bug.

### C06 Spectre testbench instance/source syntax

- Count: 1 (0.6% of failures)
- Top categories: Data Converter Models (1)
- Top forms: tb (1)
- Interpretation: The candidate testbench has malformed Spectre instance, source, include, or save syntax.
- Recommended action: This is model TB-generation failure when wrapper extraction/staging is already ruled out.

### C07 Unsupported event-loop/timer form

- Count: 1 (0.6% of failures)
- Top categories: Comparator and Decision Circuits (1)
- Top forms: dut (1)
- Interpretation: The candidate uses an event-loop form unsupported by the current evaluator/Spectre-compatible subset.
- Recommended action: Keep as model subset failure unless an EVAS core regression reproduces a Spectre-accepted construct.

### G01 Incomplete generation under fixed output budget

- Count: 4 (2.3% of failures)
- Top categories: PLL Clock and Timing Systems (3), Sampling and Analog Memory (1)
- Top forms: bugfix (2), e2e (2)
- Interpretation: The model hit the output budget or extraction ended with no usable artifact.
- Recommended action: Count as model failure under the fixed baseline budget, but keep separate from Verilog-A competence.

## Notes

- This is a deterministic, evidence-driven clustering pass over the current full236 overlay.
- Pass rows are excluded from the cluster denominator.
- Incomplete generations are counted as model failures under the fixed output budget, but are separated from Verilog-A syntax and circuit behavior failures.
- No runner/evaluator inconclusive rows and no EVAS/Spectre parity-debt rows are present in this input report.
