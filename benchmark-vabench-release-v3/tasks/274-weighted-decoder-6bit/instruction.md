# Weighted Decoder 6bit

Implement a six-input voltage-coded weighted decoder.

## Public Interface

Declare module `weighted_decoder_6bit` with positional ports `vd1, vd2, vd3,
vd4, vd5, vd6, vout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for each input bit.
- `vref = 1.0 V`: output full-scale/reference voltage.

## Functional Contract

Treat each input as logic `1` when its voltage is greater than `vth`, otherwise
logic `0`. Interpret `vd1` through `vd6` as an unsigned binary word with `vd1`
as the most significant bit and `vd6` as the least significant bit. The output
voltage should represent that decoded binary value scaled by `vref`, with the
all-ones input code corresponding to full scale.

## Modeling Constraints

Return only `weighted_decoder_6bit.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.
