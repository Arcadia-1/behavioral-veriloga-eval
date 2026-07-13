# Two Period Sample Delay

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `two_period_sample_delay.va`: `two_period_sample_delay`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TWO_PERIOD_DELAY_STATE`: On each rising `update` crossing through `vth`, `aout` updates to the value sampled on the previous update event, then captures the current `ain` for the next event.
- `P_INITIAL_OUTPUT_VALUE`: Before enough update events have occurred, the retained samples and `aout` start from `init`.
- `P_OUTPUT_GAIN_AND_HOLD`: The held `aout` value matches the delayed sample amplitude without gain scaling between update events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `two_period_sample_delay.va`.
Do not add or omit artifacts.
