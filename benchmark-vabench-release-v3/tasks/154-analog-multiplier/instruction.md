# Analog Multiplier

## Task Contract
Implement the Verilog-A DUT `analog_multiplier_gain.va` for a two-input analog voltage multiplier with a gain factor.

## Form-Specific Requirements
This is a single-DUT analog arithmetic task. Do not specialize the model to the public stimulus waveform.

## Public Verilog-A Interface
Provide `module analog_multiplier_gain(sigin1, sigin2, sigout);` with electrical inputs `sigin1`, `sigin2` and electrical output `sigout`.

## Public Parameter Contract
Expose `parameter real gain = 1;`. Testbenches may override this parameter.

## Required Behavior
Drive `sigout` to `gain * V(sigin1) * V(sigin2)` for positive and negative input products.

## Modeling Constraints
Use continuous voltage-domain arithmetic. Do not replace multiplication with addition, squaring, clipping, or a fixed waveform table.

## Output Contract
Submit only the completed Verilog-A module in `analog_multiplier_gain.va`.
