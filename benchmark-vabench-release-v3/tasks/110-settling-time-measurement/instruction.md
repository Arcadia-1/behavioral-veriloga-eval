# Settling Time Measurement

Implement `settling_time_measurement_tb.va` in Verilog-A.

## Interface

```verilog
module settling_time_measurement_tb(step,vout,done);
```

## Required Behavior

This task asks for the `settling_time_measurement_tb` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l1_settling_time_detector` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

# Task: vbm1_settling_time_measurement_tb_tb

Write a Spectre testbench for a settling response measurement helper DUT.

The DUT module is `settling_time_measurement_tb` with ports `step, vout, done`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `settling_time_measurement_tb.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 1 ns timer update with `y += 0.04 * (V(step) - y)` to model a settling response.
- Drive `vout` from `y`; assert `done` only after 120 ns and once `y` is above 0.75 V.
- This is a measurement-helper behavior task, not a true bugfix task.

Stimulus and observability requirements:
- Apply a step input and run past the 120 ns settling boundary.
- Save `step`, `vout`, and `done` with enough samples before and after the boundary.

Review caveat: This is a normal measurement-helper behavior task. It is not a bugfix task; exact 120 ns boundary semantics belong in conformance.

Return exactly one Spectre testbench file named `tb_settling_time_measurement_tb_ref.scs`.

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
