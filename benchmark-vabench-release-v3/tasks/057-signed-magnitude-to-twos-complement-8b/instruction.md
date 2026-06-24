# Signed Magnitude To Twos Complement 8b

Implement one Verilog-A DUT file named `signmag_to_twos_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `signmag_to_twos_8b` with scalar electrical ports in this exact order:

```text
sign, mag6, mag5, mag4, mag3, mag2, mag1, mag0, y7, y6, y5, y4, y3, y2, y1, y0
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold.

Convert sign-magnitude input to 8-bit two's-complement output. `sign=0` preserves `mag6..mag0` as a positive value. `sign=1` outputs the two's-complement negative value for nonzero magnitude. Negative zero must map to output zero.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A voltage contributions such as `transition(...)`.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise boundary and invalid cases.

## Output

Return exactly one source artifact named `signmag_to_twos_8b.va`. Do not generate a Spectre testbench for this task.
