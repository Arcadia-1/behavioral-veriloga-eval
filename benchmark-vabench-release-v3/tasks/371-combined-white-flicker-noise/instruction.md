# Combined White Flicker Noise

Implement one behavioral Verilog-A source file named `combined_white_flicker_noise.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module combined_white_flicker_noise (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Combine white_noise() and flicker_noise() in one behavioral source.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `combined_white_flicker_noise.va`.
