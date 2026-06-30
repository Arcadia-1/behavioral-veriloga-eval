# Flicker Noise Corner Selector

Implement one behavioral Verilog-A source file named `flicker_noise_corner_selector.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module flicker_noise_corner_selector (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Select flicker_noise() strength with a voltage-domain control.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `flicker_noise_corner_selector.va`.
