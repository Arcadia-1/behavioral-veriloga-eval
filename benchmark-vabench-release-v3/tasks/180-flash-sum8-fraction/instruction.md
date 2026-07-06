# Flash Sum8 Fraction

## Task Contract
Implement the Verilog-A DUT `flash_sum8_fraction.va` for a clocked eight-input thermometer fraction summarizer.

## Public Verilog-A Interface
Provide `module flash_sum8_fraction(din0, din1, din2, din3, din4, din5, din6, din7, clks, dout);` with electrical inputs `din0` through `din7`, clock input `clks`, and electrical output `dout`.

## Public Parameter Contract
Expose `parameter real vth = 0.45;`. Testbenches may override this threshold.

## Required Behavior
On each rising crossing of `clks` through `vth`, count how many of the eight inputs are above `vth`, divide the count by eight, and hold that fraction on `dout` until the next clock event.

## Modeling Constraints
Use clocked sampling of all eight inputs and `transition` for `dout`. Do not ignore upper inputs, use the wrong normalization, add an output offset, or continuously track the thermometer code.

## Output Contract
Submit only the completed Verilog-A module in `flash_sum8_fraction.va`.
