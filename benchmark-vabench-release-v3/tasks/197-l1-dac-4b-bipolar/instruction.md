# L1 DAC 4b Bipolar

## Task Contract
Implement the Verilog-A DUT `l1_dac_4b_bipolar.va` for a ready-clocked bipolar 4-bit DAC.

## Public Verilog-A Interface
Provide `module l1_dac_4b_bipolar(din1, din2, din3, din4, rdy, aout);` with electrical bit inputs `din1` through `din4`, ready input `rdy`, and electrical output `aout`.

## Public Parameter Contract
Expose real parameters `vdd = 1` and `vth = 0.5`. Testbenches may override these parameters.

## Required Behavior
On each rising crossing of `rdy` through `vth`, decode `din4` as the MSB and `din1` as the LSB of a 4-bit unipolar binary fraction. Map that fraction into the bipolar range by applying a `2*fraction - 1` transform and scaling by `vdd`.

## Modeling Constraints
Use clocked code sampling and `transition` for the output. Do not leave the output unipolar, omit the `vdd` scale, reverse bit weights, or continuously track input bit changes.

## Output Contract
Submit only the completed Verilog-A module in `l1_dac_4b_bipolar.va`.
