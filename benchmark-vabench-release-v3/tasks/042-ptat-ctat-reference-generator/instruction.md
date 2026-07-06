# PTAT/CTAT Reference Generator

## Task Contract

Implement the requested Verilog-A artifact for `PTAT CTAT Reference Generator`.
- Form: `dut`
- Level: `L1`
- Category: `bias_reference_power_management`
- Target artifact(s): `ptat_ctat_reference_generator.va`

Implement a clocked voltage-domain PTAT/CTAT reference macro model. Return only the requested DUT artifact; do not generate a Spectre testbench.

## Public Verilog-A Interface

```verilog
module ptat_ctat_reference_generator(clk, rst, vin, out, metric);
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
- Treat `vin` as a normalized temperature/control voltage in the 0 V to 0.9 V range.
- Build opposing PTAT and CTAT branch abstractions.
- Drive `metric` as a public PTAT-like observable that increases with the temperature/control voltage.
- Combine PTAT and CTAT behavior so `out` stays near a bounded reference around mid-scale instead of strongly tracking `vin`.
- Reset should initialize `out` near mid-scale and keep `metric` low until valid updates occur.
- Clamp `out` and `metric` to the public 0 V to 0.9 V voltage-domain range.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `ptat_ctat_reference_generator.va`.
Do not include explanatory prose outside the source artifact contents.
