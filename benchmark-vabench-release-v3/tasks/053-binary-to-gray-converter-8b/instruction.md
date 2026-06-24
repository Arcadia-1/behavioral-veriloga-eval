# Binary To Gray Converter 8b

Implement one Verilog-A DUT file named `bin_to_gray_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `bin_to_gray_8b` with scalar electrical ports in this exact order:

```text
b7, b6, b5, b4, b3, b2, b1, b0, g7, g6, g5, g4, g3, g2, g1, g0
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Convert binary input `b7..b0` into Gray-code output `g7..g0`, where `g7 = b7` and each lower Gray bit is the XOR of adjacent binary bits.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `bin_to_gray_8b.va`. Do not generate a Spectre testbench for this task.
