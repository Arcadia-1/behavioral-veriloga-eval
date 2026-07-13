# Duty-cycle Window Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `duty_cycle_window_monitor.va`: `duty_cycle_window_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear duty metric, window flag, and `valid`.
- `P_MEASURE_HIGH_AND_LOW_INTERVALS_OVER`: Measure high and low intervals over complete clock cycles using threshold crossings.
- `P_DRIVE_DUTY_METRIC_AS_THE_MEASURED`: Drive `duty_metric` as the measured high-time fraction mapped to the public voltage range.
- `P_ASSERT_IN_WINDOW_ONLY_WHEN_THE`: Assert `in_window` only when the measured duty lies between `duty_min` and `duty_max`.
- `P_ASSERT_VALID_AFTER_A_COMPLETE_HIGH`: Assert `valid` after a complete high/low cycle has been observed.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `duty_cycle_window_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
