# Binary To Thermometer Decoder 8b

Implement one Verilog-A DUT file named `bin_to_therm_8b.va`.

The DUT is a voltage-domain utility decoder used by analog/mixed-signal testbenches to expand an 8-bit binary code into a 256-line thermometer bus.

## Interface

The file must define module `bin_to_therm_8b` with scalar electrical ports in this exact order:

```text
en, b7, b6, b5, b4, b3, b2, b1, b0, th255, th254, ..., th0
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat `en` and `b7..b0` as 0/0.9 V logic using the `vth` threshold. Decode `b7..b0` as an unsigned integer code from 0 to 255, where `b7` is the most significant bit.

When `en` is high:

- drive exactly `code` thermometer outputs high;
- the high outputs must be cumulative from the low end of the bus: `th0` through `th(code-1)` are high;
- `th(code)` through `th255` are low;
- for code 0, all thermometer outputs are low;
- for code 255, `th0` through `th254` are high and `th255` is low.

When `en` is low, drive all thermometer outputs low regardless of the binary code.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test compiles the starter and runs a small Spectre-compatible EVAS transient testbench. It checks only that the module interface and simulation path are viable. Hidden tests exercise enable gating and multiple binary codes.

## Output

Return exactly one source artifact named `bin_to_therm_8b.va`. Do not generate a Spectre testbench for this task.
