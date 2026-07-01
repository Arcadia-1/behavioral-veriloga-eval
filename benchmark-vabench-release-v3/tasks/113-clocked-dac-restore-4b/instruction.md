# Clocked DAC Restore 4b

Implement a clocked 4-bit mid-rise bipolar DAC reconstruction block.

## Public Interface

Declare module `clocked_dac_restore_4b` with positional ports `D3, D2, D1,
D0, CLK, VOUT`. All ports are electrical. `D3` is the most significant bit and
`D0` is the least significant bit.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: decision threshold for `CLK` and input bits.
- `lsb = 1.8 / 16 V`: DAC least-significant-bit step.
- `tr = 20 ps`: output transition smoothing time.

## Functional Contract

On each rising `CLK` edge, latch the 4-bit input code. Drive `VOUT` as a
mid-rise bipolar DAC level: the selected level is centered around zero, uses a
half-LSB offset inside each code bin, and spans the nominal `-0.9 V` to `+0.9 V`
range across the 16 codes.

Hold the reconstructed output between clock edges.

## Modeling Constraints

Return only `clocked_dac_restore_4b.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, `ddt()`, or
`idt()`.
