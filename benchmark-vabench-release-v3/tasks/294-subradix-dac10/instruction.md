# Subradix DAC10

Implement a 10-bit voltage-coded sub-radix weighted DAC.

## Public Interface

Declare module `subradix_dac10` with positional ports `vd9, vd8, vd7, vd6,
vd5, vd4, vd3, vd2, vd1, vd0, vout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for each input bit.
- `vref = 1.0 V`: output full-scale/reference voltage.

## Functional Contract

Treat each input as logic `1` when its voltage is greater than `vth`, otherwise
logic `0`. Interpret `vd9` through `vd0` as a sub-radix word with `vd9` as the
most significant bit and `vd0` as the least significant bit. Adjacent bit
weights follow radix `1.8`. The output voltage should represent that decoded
sub-radix value scaled by `vref`, with the all-ones input code corresponding to
full scale.

## Modeling Constraints

Return only `subradix_dac10.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add checker logic, hard-code private waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`.
