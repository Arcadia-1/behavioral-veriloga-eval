# Ac Stim Phase Selector

Implement one behavioral Verilog-A source file named `ac_stim_phase_selector.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module ac_stim_phase_selector (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Select ac_stim() phase from a behavioral control voltage.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `ac_stim_phase_selector.va`.
