# Coarse 3-Bit Quantizer With Residue

Implement a continuous coarse 3-bit voltage quantizer with residue output.

## Public Interface

Declare module `coarse_qtz_3bit_residue` with positional ports `vin, d0,
d1, d2, vres`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vref = 1.0 V`: positive and negative clipping magnitude for the input
  range.
- `vdd = 1.0 V`: high output level for the binary code bits.

## Functional Contract

Clip `vin` to the parameterized range from `-vref` to `+vref`. Quantize the
clipped value into eight 3-bit codes using round-to-nearest behavior and
saturate the code at the endpoints. Use uniformly spaced quantization levels
starting at `-vref` with one LSB equal to one eighth of the full input span; the
top code level is one LSB below `+vref`.

Drive `d0` as the least significant bit, `d1` as the middle bit, and `d2` as
the most significant bit using output levels `0` and `vdd`. Drive `vres` as the
clipped input minus the selected quantized analog level.

## Modeling Constraints

Return only `coarse_qtz_3bit_residue.va`. Use deterministic voltage-domain
Verilog-A. Do not modify or emit the support testbench, add checker logic,
hard-code private waveform sample points, add simulator-private side channels,
use current contributions, `ddt()`, or `idt()`.
