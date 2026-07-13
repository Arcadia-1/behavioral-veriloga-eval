# Absolute Value

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `absolute_value_behavior.va`: `absolute_value_behavior`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_POSITIVE_INPUT_PASSTHROUGH`: For nonnegative `V(sigin)`, drive `sigout` to the same nonnegative voltage.
- `P_NEGATIVE_INPUT_REFLECTION`: For negative `V(sigin)`, drive `sigout` to `-V(sigin)`.
- `P_MEMORYLESS_ABSOLUTE_VALUE`: The output is an instantaneous absolute-value function of `sigin` with no retained state or waveform schedule.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `absolute_value_behavior.va`.
Do not add or omit artifacts.
