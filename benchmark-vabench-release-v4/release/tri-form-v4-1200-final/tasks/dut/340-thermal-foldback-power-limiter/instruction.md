# Thermal Foldback Power Limiter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `thermal_foldback_power_limiter_top.va`: `thermal_foldback_power_limiter_top`
- `foldback_controller.va`: `foldback_controller`
- `command_limiter.va`: `command_limiter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear limited command, foldback metric, and status.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, compare `temp_sense` against the foldback threshold.
- `P_PASS_POWER_CMD_THROUGH_WHILE_TEMPERATURE`: Pass `power_cmd` through while temperature is below threshold.
- `P_REDUCE_LIMITED_CMD_AS_TEMPERATURE_RISES`: Reduce `limited_cmd` as temperature rises above threshold and expose the reduction on `foldback_metric`.
- `P_ASSERT_THERMAL_OK_ONLY_WHEN_NO`: Assert `thermal_ok` only when no foldback reduction is active.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `thermal_foldback_power_limiter_top.va`, `foldback_controller.va`, `command_limiter.va`.
Do not add or omit artifacts.
