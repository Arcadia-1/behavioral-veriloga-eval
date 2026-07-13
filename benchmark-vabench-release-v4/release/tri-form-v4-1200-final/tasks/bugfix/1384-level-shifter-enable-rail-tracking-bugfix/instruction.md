# Level Shifter with Enable and Rail Tracking Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `level_shifter_enable_rail_tracking.va`: `level_shifter_enable_rail_tracking`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to `vss` and clears `valid`.
- `P_WHEN_ENABLED_COMPARE_VIN_AGAINST_HALF`: When enabled, compare `vin` against half of the sensed low-side rail `vddl`.
- `P_DRIVE_VOUT_TO_VDDH_FOR_A`: Drive `vout` to `vddh` for a high input and to `vss` for a low input.
- `P_VALID_IS_HIGH_ONLY_WHEN_ENABLED`: `valid` is high only when enabled, not reset, and the high-side rail is above the minimum valid rail.
- `P_THE_OUTPUT_HIGH_LEVEL_MUST_TRACK`: The output high level must track changes in `vddh`; it must not use a fixed internal high level.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `level_shifter_enable_rail_tracking.va`.
Every supplied `.va` file is editable; do not add or omit files.
