# Onehot To Binary Encoder 16b

Implement one Verilog-A DUT file named `onehot_to_bin_16b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `onehot_to_bin_16b` with scalar electrical ports in this exact order:

```text
oh15, oh14, oh13, oh12, oh11, oh10, oh9, oh8, oh7, oh6, oh5, oh4, oh3, oh2, oh1, oh0, b3, b2, b1, b0, valid
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Encode a 16-line one-hot input `oh15..oh0` into binary index `b3..b0`. Drive `valid` high only when exactly one input is high. For zero-hot or multi-hot inputs, drive `valid` low and drive `b3..b0` to zero.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `onehot_to_bin_16b.va`. Do not generate a Spectre testbench for this task.
