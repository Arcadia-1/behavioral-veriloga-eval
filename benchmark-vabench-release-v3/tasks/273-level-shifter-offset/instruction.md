# Level Shifter Offset

## Task Contract
Implement the Verilog-A DUT `level_shifter_offset.va` for a continuous analog level shifter.

## Form-Specific Requirements
This is a single-DUT analog primitive task. The input waveform may vary; the output must always apply the public offset parameter.

## Public Verilog-A Interface
Provide `module level_shifter_offset(sigin, sigout);` with electrical input `sigin` and electrical output `sigout`.

## Public Parameter Contract
Expose `parameter real sigshift = 0.35;`. Testbenches may override this parameter.

## Required Behavior
Drive `sigout` to `V(sigin) + sigshift`.

## Modeling Constraints
Use direct continuous voltage-domain arithmetic. Do not invert the offset, add gain, clip the output, or add hidden state.

## Output Contract
Submit only the completed Verilog-A module in `level_shifter_offset.va`.
