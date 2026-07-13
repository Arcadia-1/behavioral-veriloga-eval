# Logarithmic Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `logarithmic_amplifier.va`: `logarithmic_amplifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INPUT_OFFSET_SUBTRACTION`: Subtract 0.2 V from `V(sigin)` before computing magnitude.
- `P_ABSOLUTE_MAGNITUDE`: Use the absolute value of the offset-corrected voltage as the logarithm argument magnitude.
- `P_MAGNITUDE_FLOOR`: Floor the magnitude at 0.1 V before applying the logarithm.
- `P_NATURAL_LOG_OUTPUT`: Drive `sigout` to the natural logarithm of the guarded magnitude.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `logarithmic_amplifier.va`.
Do not add or omit artifacts.
