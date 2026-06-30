# Flicker Noise Voltage Source

Implement one behavioral Verilog-A source file named `flicker_noise_voltage_source.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module flicker_noise_voltage_source (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use flicker_noise() as a behavioral 1/f noise contribution.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `flicker_noise_voltage_source.va`.
