# Hysteretic Window Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `hysteretic_window_comparator.va`: `hysteretic_window_comparator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `inside_flag`, `state_metric`, and `toggled`.
- `P_USE_LOW_TRIP_AND_HIGH_TRIP`: Use `low_trip` and `high_trip` as public voltage thresholds.
- `P_ASSERT_INSIDE_FLAG_WHEN_VIN_ENTERS`: Assert `inside_flag` when `vin` enters the window and keep it asserted until `vin` crosses outside the hysteresis margins.
- `P_EXPOSE_THE_CURRENT_STATE_AS_STATE`: Expose the current state as `state_metric` and pulse `toggled` high on state changes.
- `P_DO_NOT_CHATTER_FOR_SMALL_INPUT`: Do not chatter for small input movement inside the hysteresis band.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `hysteretic_window_comparator.va`.
Do not add or omit artifacts.
