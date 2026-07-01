# Analysis Dependent Dc Tran Mode

Implement one behavioral Verilog-A source file named `analysis_dependent_dc_tran_mode.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module analysis_dependent_dc_tran_mode (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use analysis() to choose DC versus transient behavior.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `analysis_dependent_dc_tran_mode.va`.
