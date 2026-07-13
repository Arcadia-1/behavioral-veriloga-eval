# Thermal Foldback Power Limiter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `thermal_foldback_power_limiter_top.va`: `thermal_foldback_power_limiter_top`
- `foldback_controller.va`: `foldback_controller`
- `command_limiter.va`: `command_limiter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear limited command, foldback metric, and status.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, compare `temp_sense` against the foldback threshold.
- `P_PASS_POWER_CMD_THROUGH_WHILE_TEMPERATURE`: Pass `power_cmd` through while temperature is below threshold.
- `P_REDUCE_LIMITED_CMD_AS_TEMPERATURE_RISES`: Reduce `limited_cmd` as temperature rises above threshold and expose the reduction on `foldback_metric`.
- `P_ASSERT_THERMAL_OK_ONLY_WHEN_NO`: Assert `thermal_ok` only when no foldback reduction is active.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `thermal_foldback_power_limiter_top.va`, `foldback_controller.va`, `command_limiter.va`.
Every supplied `.va` file is editable; do not add or omit files.
