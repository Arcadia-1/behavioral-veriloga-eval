# Binary To Onehot Decoder 16b

Implement one Verilog-A DUT file named `bin_to_onehot_16b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `bin_to_onehot_16b` with scalar electrical ports in this exact order:

```text
en, b3, b2, b1, b0, oh15, oh14, oh13, oh12, oh11, oh10, oh9, oh8, oh7, oh6, oh5, oh4, oh3, oh2, oh1, oh0
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Decode binary input `b3..b0` into one-hot output `oh15..oh0` when `en` is high. Exactly one output, `oh(code)`, must be high. When `en` is low, all one-hot outputs must be low.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `bin_to_onehot_16b.va`. Do not generate a Spectre testbench for this task.
