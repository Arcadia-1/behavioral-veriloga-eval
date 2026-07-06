# Bandgap Reference Macro Model

## Task Contract

Implement the requested Verilog-A artifact for `Bandgap Reference Macro Model`.
- Form: `dut`
- Level: `L1`
- Category: `bias_reference_power_management`
- Target artifact(s): `bandgap_reference_macro_model.va`

Implement a clocked voltage-domain bandgap/reference macro model with startup validity reporting. Return only the requested DUT artifact; do not generate a Spectre testbench.

## Public Verilog-A Interface

```verilog
module bandgap_reference_macro_model(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 100 ps`: output transition rise/fall smoothing time.
- `vth = 0.45 V`: voltage-coded logic threshold for `clk` and `rst`.
- `vstart = 0.58 V`: startup supply threshold for `vin`.
- `vref = 0.55 V`: nominal regulated reference target.

## Required Behavior

- `clk` and `rst` are voltage-coded logic signals, low near 0 V and high near 0.9 V.
- `vin` is a sub-1 V supply ramp for the reference macro.
- During reset or below the startup threshold, hold `out` near 0 V and keep `metric` low.
- After startup, regulate `out` near the nominal reference voltage and make it weakly sensitive to supply variation rather than supply-tracking.
- During brownout, return `out` near 0 V and mark the reference invalid.
- Drive `metric` as a voltage-coded reference-valid observable: low before startup/brownout, high while the reference is valid.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `bandgap_reference_macro_model.va`.
Do not include explanatory prose outside the source artifact contents.
