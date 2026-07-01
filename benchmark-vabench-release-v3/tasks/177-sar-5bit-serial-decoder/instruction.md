# SAR 5-Bit Serial Decoder

Implement a voltage-coded serial SAR decision decoder.

## Public Interface

Declare module `sar_5bit_serial_decoder` with positional ports `din, clks,
ready, dout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.55 V`: digital decision threshold for `din`, `ready`, and `clks`.
- `nbit = 5`: number of serial SAR decisions in one conversion.

## Functional Contract

Decode one SAR conversion from five serial comparator decisions. On each rising
`ready` edge, sample `din` against `vth` and add the current binary weight,
starting with the most significant bit and descending to the least significant
bit.

On each rising `clks` edge, publish the accumulated code on `dout` as a
centered normalized value over the full 5-bit range: the all-zero conversion
maps to `-0.5`, and the all-ones conversion maps to `+0.5`. After publishing,
clear the accumulator and restart the bit counter for the next conversion.

## Modeling Constraints

Return only `sar_5bit_serial_decoder.va`. Use deterministic voltage-domain
Verilog-A and a smooth output transition after each published code update. Do
not modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.
