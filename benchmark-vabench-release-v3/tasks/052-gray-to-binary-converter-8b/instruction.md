# Gray To Binary Converter 8b

Implement one Verilog-A DUT file named `gray_to_bin_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `gray_to_bin_8b` with scalar electrical ports in this exact order:

```text
g7, g6, g5, g4, g3, g2, g1, g0, b7, b6, b5, b4, b3, b2, b1, b0
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Convert Gray-code input `g7..g0` into binary output `b7..b0`, where `g7` and `b7` are most significant bits.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `gray_to_bin_8b.va`. Do not generate a Spectre testbench for this task.
