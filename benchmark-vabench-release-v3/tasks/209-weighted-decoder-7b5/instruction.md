# Weighted Decoder 7b5

Implement a voltage-coded bipolar SAR decision decoder that reports 7-bit,
7.5-bit, and 8-bit weighted analog reconstructions from the same decision
inputs.

## Public Interface

Declare module `weighted_decoder_7b5` with positional ports `d0, d1, d2, d3,
d4, d5, d6, d7, d8, aout7b, aout7b5, aout8b`. All ports are electrical.
`d0..d8` are inputs, and `aout7b`, `aout7b5`, and `aout8b` are outputs.

## Public Parameter Contract

Provide this overrideable public parameter:

- `vth = 0.5 V`: digital decision threshold for each input bit.

## Functional Contract

Treat each input as a bipolar decision bit: logic high when its voltage is
greater than `vth` maps to `+1`, and logic low maps to `-1`.

Drive three weighted reconstruction outputs using the same redundant SAR
ladder. From low to high order, the shared ladder uses weights `1, 2, 4, 8, 8,
16, 32, 64` for `d1..d8`; the repeated weight-8 term is intentional.

- `aout7b` uses the shared ladder from `d1..d8`.
- `aout8b` adds `d0` as a half-weight refinement below `d1`.
- `aout7b5` replaces the `d1` LSB contribution with a three-level `d0`/`d1`
  paired decision: `+1` when both are high, `-1` when both are low, and `0`
  when they differ.

Normalize all three outputs against the same redundant SAR array basis. The
normalization basis includes the shared `d1..d8` ladder plus one fixed
unit/reference element, and uses the full bipolar range of that basis. Do not
introduce separate per-output normalization scales; the three reconstructed
outputs should remain centered around zero and comparable to one another.

## Modeling Constraints

Return only `weighted_decoder_7b5.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.
