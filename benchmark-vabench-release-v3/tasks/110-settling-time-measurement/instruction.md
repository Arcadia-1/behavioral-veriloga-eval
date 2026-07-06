# Settling Time Measurement

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Measurement Helper
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `settling_time_measurement_tb.va`
- Required module: `settling_time_measurement_tb`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Do not generate a Spectre `.scs` file, checker, waveform file, or extra support artifact.
- Preserve the public module name, port order, and observable names.

## Public Verilog-A Interface

```verilog
module settling_time_measurement_tb(step, vout, done);
```

All ports are electrical. `step` is the input step stimulus, `vout` is the
settling-response output, and `done` is a voltage-coded completion flag.

## Public Parameter Contract

- `tr = 300p`: transition smoothing time for `vout` and `done`.

## Required Behavior

Use a 1 ns timer update to model a first-order settling response:

```text
y += 0.04 * (V(step) - y)
```

Drive `vout` from the internal state `y`. Drive `done` low before the settling
boundary and high only after simulation time is beyond 120 ns and the settled
state is above 0.75 V. Use low output near 0 V and high output near 0.9 V. The
public observable waveforms are `step`, `vout`, and `done`.

## Modeling Constraints

Use pure behavioral Verilog-A with voltage-domain outputs and `transition()`.
Do not use transistor-level devices, AC/noise analysis, current contributions,
waveform-file IO, checker artifacts, simulator-specific side channels, `ddt()`,
or `idt()`.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`settling_time_measurement_tb.va`. Do not include explanatory prose outside the
source artifact contents.
