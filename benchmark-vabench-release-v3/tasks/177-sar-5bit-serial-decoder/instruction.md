# SAR 5bit Serial Decoder

## Task Contract
Implement the Verilog-A DUT `sar_5bit_serial_decoder.va` for a voltage-coded serial SAR decision decoder.

## Public Verilog-A Interface
Provide `module sar_5bit_serial_decoder(din, clks, ready, dout);` with electrical inputs `din`, `clks`, `ready` and electrical output `dout`.

## Public Parameter Contract
Expose real parameter `vth = 0.55` and integer parameter `nbit = 5`. Testbenches may override these parameters.

## Required Behavior
After each publication clock, collect up to `nbit` serial decision bits on rising `ready` crossings, MSB first. A high `din` adds the current binary weight and a low `din` adds zero. On each rising `clks` crossing, publish the accumulated unsigned SAR code normalized to the `nbit` full-scale range and centered by subtracting 0.5, then reset the accumulator for the next conversion.

## Modeling Constraints
Use event-driven ready and clock handling. Do not reverse the serial weights, omit the midscale centering, use the wrong normalization, or continuously update `dout` on `din` changes.

## Output Contract
Submit only the completed Verilog-A module in `sar_5bit_serial_decoder.va`.
