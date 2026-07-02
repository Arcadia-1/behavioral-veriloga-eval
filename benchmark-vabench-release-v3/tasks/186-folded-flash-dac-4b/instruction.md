# Folded 4-Bit Flash DAC

Implement a voltage-coded folded 4-bit flash DAC.

## Public Interface

Declare module `folded_flash_dac_4b` with positional ports `vd4, vd3, vd2,
vd1, vout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vref = 1.0 V` from `[0:inf]`: output reference scale.
- `vtrans = 0.45 V`: digital decision threshold for each input bit.
- `trise = 1 ps` from `[0:inf]`: output transition rise time.
- `tfall = 1 ps` from `[0:inf]`: output transition fall time.
- `tdel = 0 s` from `[0:inf]`: output transition delay.

## Functional Contract

Treat each input as logic `1` when its voltage is greater than `vtrans`,
otherwise logic `0`. The lower three bits `vd3..vd1` form a binary subcode
with weights 4, 2, and 1. The MSB `vd4` selects the folded branch: when `vd4`
is high, the folded code is the upper branch `8 + subcode`; when `vd4` is low,
the folded code is the mirrored branch `8 - subcode`.

Scale the folded code by `vref` over a 16-step DAC range and drive `vout`
through the parameterized transition timing.

## Modeling Constraints

Return only `folded_flash_dac_4b.va`. Use deterministic voltage-domain
Verilog-A. Do not modify or emit the support testbench, add checker logic,
hard-code private waveform sample points, add simulator-private side channels,
use current contributions, `ddt()`, or `idt()`.
