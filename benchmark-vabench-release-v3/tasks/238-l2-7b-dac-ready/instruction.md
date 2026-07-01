# Ready-Triggered 7-bit Capacitive DAC

Implement a ready-triggered 7-bit single-ended capacitive weighted DAC.

## Public Interface

Declare module `l2_7b_dac_ready` with positional ports `din1, din2, din3,
din4, din5, din6, din7, rdy, aout`. All ports are electrical. `din1..din7`
and `rdy` are inputs, and `aout` is the output.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: output scaling reference for the bipolar single-ended output.
- `vth = 0.45 V`: digital decision threshold for each input bit and the ready
  edge detector.

## Functional Contract

Use rising crossings of `rdy` through `vth` as the update event. The first
ready edge only arms the DAC and must leave the output state at its initialized
`0 V` value. On each later ready edge, sample `din1..din7`. Treat each input
as logic `1` when its voltage is greater than `vth`, otherwise logic `0`.

Decode the sampled inputs with switched capacitor weights:

- `din7`: 32
- `din6`: 16
- `din5`: 8
- `din4`: 4
- `din3`: 2
- `din2`: 1
- `din1`: 0.5

The DAC normalization includes one additional fixed, non-switching unit
capacitance. This fixed unit contributes to the total normalization weight but
is not controlled by any input bit.

Drive `aout` as a bipolar single-ended voltage scaled by `vdd` from the ratio
between the sampled switched capacitance and the total capacitance. An all-zero
sampled code drives the negative endpoint near `-vdd`; an all-one sampled code
remains below `+vdd` because the fixed unit capacitance is included in the
normalization.

## Modeling Constraints

Return only `l2_7b_dac_ready.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add checker logic, hard-code private waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`.
