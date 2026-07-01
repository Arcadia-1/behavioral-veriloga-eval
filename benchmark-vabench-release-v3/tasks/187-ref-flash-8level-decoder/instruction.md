# Reference Flash 8-Level Decoder With Residue

Implement an 8-level reference flash decoder with residue output.

## Public Interface

Declare module `ref_flash_8level_decoder` with positional ports `vin, dt0,
dt1, dt2, dt3, dt4, dt5, dt6, dt7, clks, dout, vres`. All ports are
electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for thermometer taps and rising
  edge threshold for `clks`.
- `vref = 1.0 V`: reference step scale for the residue correction.
- `tt = 10 ps`: output transition smoothing time.

## Functional Contract

On each rising `clks` edge, count thermometer taps `dt0..dt7` whose voltages
are greater than `vth`. Drive `dout` with the count normalized by eight.

Also compute a centered residue around the mid-code reference: four asserted
taps represent zero correction, and each tap step corresponds to `vref/8`.
Drive `vres` as the sampled input minus that centered reference correction.

## Modeling Constraints

Return only `ref_flash_8level_decoder.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, `ddt()`, or
`idt()`.
