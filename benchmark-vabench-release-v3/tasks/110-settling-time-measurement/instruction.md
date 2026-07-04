# Settling Time Measurement

Implement `settling_time_measurement_tb.va` in Verilog-A.

## Interface

```verilog
module settling_time_measurement_tb(step, vout, done);
```

Inputs:

- `step`: electrical input step stimulus.

Outputs:

- `vout`: electrical settling-response output.
- `done`: electrical completion flag.

## Required Behavior

This is a measurement-helper DUT task, not a Spectre testbench-generation task.
Return only the Verilog-A source file `settling_time_measurement_tb.va`.

Use a 1 ns timer update to model a first-order settling response:

```text
y += 0.04 * (V(step) - y)
```

Drive `vout` from the internal state `y`. Drive `done` low before the settling
boundary and high only after the simulation time is beyond 120 ns and the
settled state is above 0.75 V. The evaluator applies a step input, runs past
the 120 ns boundary, and saves `step`, `vout`, and `done`.

Use voltage-coded logic with a 0.45 V threshold where applicable. Drive high
logic outputs near 0.9 V and low outputs near 0 V. Keep the model pure
behavioral Verilog-A.

Do not generate a Spectre `.scs` file. Do not use transistor-level devices,
AC/noise analysis, current contributions, waveform files, checker artifacts, or
simulator side channels.

## Output Contract

Return exactly one complete Verilog-A file named
`settling_time_measurement_tb.va`. Do not include explanatory prose outside the
source artifact contents.
