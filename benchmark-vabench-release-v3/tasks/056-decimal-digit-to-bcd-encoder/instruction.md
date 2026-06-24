# Decimal Digit To BCD Encoder

Implement one Verilog-A DUT file named `decimal_to_bcd.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `decimal_to_bcd` with scalar electrical ports in this exact order:

```text
d9, d8, d7, d6, d5, d4, d3, d2, d1, d0, b3, b2, b1, b0, valid
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Encode one-hot decimal digit input `d9..d0` into BCD output `b3..b0`. Drive `valid` high only when exactly one digit input is high. For zero-hot or multi-hot inputs, drive `valid` low and drive `b3..b0` to zero.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `decimal_to_bcd.va`. Do not generate a Spectre testbench for this task.
