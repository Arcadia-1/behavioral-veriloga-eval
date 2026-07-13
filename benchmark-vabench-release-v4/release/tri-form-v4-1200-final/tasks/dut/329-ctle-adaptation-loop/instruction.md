# CTLE Adaptation Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ctle_adaptation_loop_top.va`: `ctle_adaptation_loop_top`
- `ctle_boost_core.va`: `ctle_boost_core`
- `boost_adapt_controller.va`: `boost_adapt_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear boost code, output, metric, and `locked`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, compare `edge_metric_in` with `edge_target`.
- `P_INCREASE_BOOST_CODE_WHEN_EDGE_METRIC`: Increase boost code when edge metric is too low and decrease it when too high.
- `P_DRIVE_VOUT_AS_A_BOOSTED_VERSION`: Drive `vout` as a boosted version of `vin - vcm` using the active boost code.
- `P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `locked` after three consecutive updates within the target tolerance.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ctle_adaptation_loop_top.va`, `ctle_boost_core.va`, `boost_adapt_controller.va`.
Do not add or omit artifacts.
