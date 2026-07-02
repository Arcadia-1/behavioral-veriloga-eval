# Cyclic ADC 10-Bit Decision Decoder

Implement a voltage-coded cyclic ADC decision decoder.

## Public Interface

Declare module `cyclic_decoder_10b` with positional ports `dp, dn, ready,
clks, dout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.55 V`: digital decision threshold for `dp`, `dn`, `ready`, and
  `clks`.
- `nbit = 10`: number of cyclic ADC decision positions in one conversion.

## Functional Contract

On each rising `ready` edge, sample comparator decision inputs `dp` and `dn`
against `vth` and accumulate the current bit weight. Starting from the most
significant bit and descending toward the least significant bit, `dp` high
contributes a full binary weight, `dp` low with `dn` high contributes a half
weight, and both low contributes zero.

On each rising `clks` edge, publish the accumulated cyclic ADC code on `dout`
as a centered normalized value over the full `nbit` range: the all-zero
conversion maps to `-0.5`, and an all-full-weight conversion maps to `+0.5`.
After publishing, clear the accumulator and restart the bit counter for the
next conversion.

## Modeling Constraints

Return only `cyclic_decoder_10b.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, `ddt()`, or
`idt()`.
