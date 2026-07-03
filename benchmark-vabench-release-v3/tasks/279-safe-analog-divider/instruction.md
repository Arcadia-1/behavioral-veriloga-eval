# Safe Analog Divider

## Task Contract
Implement the Verilog-A module `safe_analog_divider.va` for an analog divider with a sign-preserving minimum denominator magnitude.

## Form-Specific Requirements
This is a small analog arithmetic component. The public contract is the divider behavior, not the specific stimulus waveform.

## Public Verilog-A Interface
Provide `module safe_analog_divider(signumer, sigdenom, sigout);` with electrical inputs `signumer`, `sigdenom` and electrical output `sigout`.

## Public Parameter Contract
Expose `gain = 1.0` and `min_sigdenom = 0.2` as real parameters. Testbenches may override these parameters.

## Required Behavior
Drive `sigout` to `gain * V(signumer) / denominator`, where `denominator` is `V(sigdenom)` unless its magnitude is below `min_sigdenom`. In that guarded region, use `+min_sigdenom` for nonnegative denominators and `-min_sigdenom` for negative denominators.

## Modeling Constraints
Use continuous voltage-domain arithmetic. Preserve denominator sign under the guard and keep the gain parameter active.

## Output Contract
Submit only the completed Verilog-A module in `safe_analog_divider.va`.
