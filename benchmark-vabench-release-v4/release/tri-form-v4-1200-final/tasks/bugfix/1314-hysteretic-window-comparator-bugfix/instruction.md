# Hysteretic Window Comparator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `hysteretic_window_comparator.va`: `hysteretic_window_comparator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `inside_flag`, `state_metric`, and `toggled`.
- `P_USE_LOW_TRIP_AND_HIGH_TRIP`: Use `low_trip` and `high_trip` as public voltage thresholds.
- `P_ASSERT_INSIDE_FLAG_WHEN_VIN_ENTERS`: Assert `inside_flag` when `vin` enters the window and keep it asserted until `vin` crosses outside the hysteresis margins.
- `P_EXPOSE_THE_CURRENT_STATE_AS_STATE`: Expose the current state as `state_metric` and pulse `toggled` high on state changes.
- `P_DO_NOT_CHATTER_FOR_SMALL_INPUT`: Do not chatter for small input movement inside the hysteresis band.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `hysteretic_window_comparator.va`.
Every supplied `.va` file is editable; do not add or omit files.
