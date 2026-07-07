# Weighted SAR Decoder 9b

## Task Contract
Implement the Verilog-A DUT `weighted_sar_decoder_9b.va` for a source-weighted SAR decoder that publishes three related centered analog summary voltages.

## Public Verilog-A Interface
Provide `module weighted_sar_decoder_9b(d0, d1, d2, d3, d4, d5, d6, d7, d8, aout7b, aout7b5, aout8b);` with electrical inputs `d0` through `d8` and electrical outputs `aout7b`, `aout7b5`, `aout8b`.

## Public Parameter Contract
Expose `parameter real vth = 0.5;`. Testbenches may override this threshold.

## Required Behavior
Interpret each decision input as a bipolar cell: above `vth` contributes +1 in its cell group and below `vth` contributes -1. The main 7-bit view uses weighted groups from `d1` through `d8`, with `d4` and `d5` representing equal split midscale groups. The 8-bit view adds `d0` as a half-LSB group. The 7.5-bit view replaces the two smallest decisions with a ternary LSB: both high gives +1, both low gives -1, and mixed values give 0.

Normalize all three centered sums by the public full source-array span `272.0`, including the fixed non-switching unit used by the source DAC array:

- `aout7b = (b1 + 2*b2 + 4*b3 + 8*b4 + 8*b5 + 16*b6 + 32*b7 + 64*b8) / 272.0`.
- `aout8b = (0.5*b0 + b1 + 2*b2 + 4*b3 + 8*b4 + 8*b5 + 16*b6 + 32*b7 + 64*b8) / 272.0`.
- `aout7b5 = (d_lsb + 2*b2 + 4*b3 + 8*b4 + 8*b5 + 16*b6 + 32*b7 + 64*b8) / 272.0`.

## Modeling Constraints
Use voltage-coded decisions and analog summary outputs. Do not treat the decision cells as unipolar bits, drop the MSB group, use separate normalizations for the three outputs, or hard-code values from a particular stimulus sequence.

## Output Contract
Submit only the completed Verilog-A module in `weighted_sar_decoder_9b.va`.
