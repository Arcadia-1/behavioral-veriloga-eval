# Level Shifter with Enable and Rail Tracking

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `level_shifter_enable_rail_tracking.va`: `level_shifter_enable_rail_tracking`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to `vss` and clears `valid`.
- `P_WHEN_ENABLED_COMPARE_VIN_AGAINST_HALF`: When enabled, compare `vin` against half of the sensed low-side rail `vddl`.
- `P_DRIVE_VOUT_TO_VDDH_FOR_A`: Drive `vout` to `vddh` for a high input and to `vss` for a low input.
- `P_VALID_IS_HIGH_ONLY_WHEN_ENABLED`: `valid` is high only when enabled, not reset, and the high-side rail is above the minimum valid rail.
- `P_THE_OUTPUT_HIGH_LEVEL_MUST_TRACK`: The output high level must track changes in `vddh`; it must not use a fixed internal high level.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `level_shifter_enable_rail_tracking.va`.
Do not add or omit artifacts.
