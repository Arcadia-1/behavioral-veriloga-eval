# Glitchless Clock Mux Selector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `glitchless_clock_mux_selector.va`: `glitchless_clock_mux_selector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `clk_out`, `switch_metric`, and `valid` low.
- `P_ROUTE_CLK_A_WHEN_SEL_IS`: Route `clk_a` when `sel` is low and `clk_b` when `sel` is high.
- `P_WHEN_SEL_CHANGES_WAIT_UNTIL_BOTH`: When `sel` changes, wait until both input clocks are low before changing the active source.
- `P_EXPOSE_A_SWITCH_EVENT_ON_SWITCH`: Expose a switch event on `switch_metric` for one output cycle after the selected source changes.
- `P_ASSERT_VALID_AFTER_THE_SELECTED_SOURCE`: Assert `valid` after the selected source has produced one clean output edge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `glitchless_clock_mux_selector.va`.
Do not add or omit artifacts.
