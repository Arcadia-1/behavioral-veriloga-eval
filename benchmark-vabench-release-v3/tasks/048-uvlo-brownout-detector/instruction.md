# UVLO Brownout Detector

## Task Contract

Implement the requested Verilog-A artifact for `UVLO Brownout Detector`.
- Form: `dut`
- Level: `L1`
- Category: `bias_reference_power_management`
- Target artifact(s): `uvlo_brownout_detector.va`

Implement a clocked voltage-domain undervoltage-lockout and brownout detector. Return only the requested DUT artifact; do not generate a Spectre testbench.

## Public Verilog-A Interface

```verilog
module uvlo_brownout_detector(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 100 ps`: output transition rise/fall smoothing time.
- `vth = 0.45 V`: voltage-coded logic threshold for `clk` and `rst`.

## Required Behavior

- `clk` and `rst` are voltage-coded logic signals.
- Treat `vin` as the monitored supply voltage.
- Assert the power-good output `out` high only after `vin` rises above the upper UVLO threshold, around 0.65 V.
- Keep `out` high while `vin` remains in the hysteresis band between the lower and upper UVLO thresholds.
- Clear `out` low on reset or brownout below the lower threshold, around 0.55 V.
- Drive `metric` to distinguish undervoltage/brownout fault from valid power-good operation.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `uvlo_brownout_detector.va`.
Do not include explanatory prose outside the source artifact contents.
