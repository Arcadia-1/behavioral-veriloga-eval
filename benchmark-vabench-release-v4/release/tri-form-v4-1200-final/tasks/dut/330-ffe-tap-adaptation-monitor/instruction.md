# FFE Tap Adaptation Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ffe_tap_adaptation_monitor_top.va`: `ffe_tap_adaptation_monitor_top`
- `tap_update_controller.va`: `tap_update_controller`
- `cursor_metric_core.va`: `cursor_metric_core`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear tap states, output, adapt metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, update pre and post tap signs according to `err_in - vcm`.
- `P_DRIVE_MAIN_OUT_AS_THE_CURRENT`: Drive `main_out` as the current main cursor correction around `vcm`.
- `P_EXPOSE_AGGREGATE_TAP_MAGNITUDE_ON_ADAPT`: Expose aggregate tap magnitude on `adapt_metric`.
- `P_ASSERT_DONE_AFTER_SIX_ENABLED_ADAPTATION`: Assert `done` after six enabled adaptation updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ffe_tap_adaptation_monitor_top.va`, `tap_update_controller.va`, `cursor_metric_core.va`.
Do not add or omit artifacts.
