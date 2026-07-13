# Duty-cycle Window Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `duty_cycle_window_monitor.va`: `duty_cycle_window_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear duty metric, window flag, and `valid`.
- `P_MEASURE_HIGH_AND_LOW_INTERVALS_OVER`: Measure high and low intervals over complete clock cycles using threshold crossings.
- `P_DRIVE_DUTY_METRIC_AS_THE_MEASURED`: Drive `duty_metric` as the measured high-time fraction mapped to the public voltage range.
- `P_ASSERT_IN_WINDOW_ONLY_WHEN_THE`: Assert `in_window` only when the measured duty lies between `duty_min` and `duty_max`.
- `P_ASSERT_VALID_AFTER_A_COMPLETE_HIGH`: Assert `valid` after a complete high/low cycle has been observed.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `duty_cycle_window_monitor.va`.
Do not add or omit artifacts.
