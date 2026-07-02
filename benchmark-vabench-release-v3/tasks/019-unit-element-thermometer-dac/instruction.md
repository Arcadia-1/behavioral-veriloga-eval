# Unit Element Thermometer DAC

Implement a 15-segment unit-element thermometer DAC.

## Public Interface

Declare module `thermometer_dac_15seg` with positional ports `seg0, seg1,
seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11, seg12, seg13,
seg14, vref, vss, aout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for each segment input.
- `tr = 500 ps`: output transition smoothing time.

## Functional Contract

Treat every segment input above `vth` as one active unit element. Count all
fifteen unary segment pins, including `seg14`. Drive `aout` between `vss` and
`vref` in proportion to the active segment count, with zero active segments at
`vss` and all fifteen active segments at `vref`.

## Modeling Constraints

Return only `thermometer_dac_15seg.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, `ddt()`, or
`idt()`.
