# Divide By Two Toggle

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `divide_by_two_toggle.va`: `divide_by_two_toggle`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_TOGGLE_STATE`: Each rising `clkin` crossing through 0.5 V toggles the retained divider state.
- `P_INITIAL_LOW_STATE`: The retained state and `clkout` start low before the first input-clock edge.
- `P_OUTPUT_RAIL_LEVELS`: `clkout` drives 0.9 V for high state and 0.0 V for low state without amplitude scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `divide_by_two_toggle.va`.
Do not add or omit artifacts.
