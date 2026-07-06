# DAC 8bit Ideal Scalar

## Task Contract
Implement the Verilog-A DUT `dac_8bit_ideal_scalar.va` for an event-updated ideal 8-bit scalar DAC.

## Public Verilog-A Interface
Provide `module dac_8bit_ideal_scalar(vd7, vd6, vd5, vd4, vd3, vd2, vd1, vd0, vout);` with electrical bit inputs `vd7` through `vd0` and electrical output `vout`.

## Public Parameter Contract
Expose real parameters `vref = 1`, `trise = 1p`, `tfall = 1p`, `tdel = 0`, and `vtrans = 2.5` with the ranges declared in the starter file. Testbenches may override these parameters.

## Required Behavior
Interpret each input as logic high above `vtrans`, with `vd7` as the MSB and `vd0` as the LSB. Decode the unsigned 8-bit code and drive `vout` to the corresponding fraction of `vref` over the 256-code range.

## Modeling Constraints
Update on input threshold crossings or initial step and drive a smooth analog output. Do not reverse bit weights, use the wrong denominator, or halve the output gain.

## Output Contract
Submit only the completed Verilog-A module in `dac_8bit_ideal_scalar.va`.
