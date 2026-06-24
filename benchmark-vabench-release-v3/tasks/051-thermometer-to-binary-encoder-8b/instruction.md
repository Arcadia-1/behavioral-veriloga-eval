# Thermometer To Binary Encoder 8b

Implement one Verilog-A DUT file named `therm_to_bin_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `therm_to_bin_8b` with scalar electrical ports in this exact order:

```text
th255, th254, ..., th0, b7, b6, ..., b0, valid
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Encode `th255..th0` into an 8-bit count and a `valid` flag. A valid thermometer input is cumulative from `th0`: exactly `th0` through `th(count-1)` are high and all higher thermometer inputs are low. For valid inputs, drive `b7..b0` to the unsigned count, where `b7` is the most significant bit. Code 0 is valid and means all thermometer inputs are low. Code 255 is valid and means `th0` through `th254` are high and `th255` is low.

For any non-cumulative bubble, gap, or isolated high pattern, drive `valid` low and drive `b7..b0` to zero.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `therm_to_bin_8b.va`. Do not generate a Spectre testbench for this task.
