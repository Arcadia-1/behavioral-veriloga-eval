# Offset Gain Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `offset_gain_amplifier.va`: `offset_gain_amplifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INPUT_OFFSET_SUBTRACTION`: Subtract 0.2 V from `V(sigin)` before applying gain.
- `P_FIXED_GAIN_THREE`: Drive `sigout` to `3.0 * (V(sigin) - 0.2)`.
- `P_DIRECT_MEMORYLESS_OUTPUT`: Use a direct memoryless voltage output without clipping, filtering, current output, or stimulus-specific behavior.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `offset_gain_amplifier.va`.
Do not add or omit artifacts.
