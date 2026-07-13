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

- `P_INITIALIZE_THE_INTERNAL_DIVIDER_STATE_LOW`: Initialize the internal divider state low.
- `P_TOGGLE_THE_STATE_ON_EVERY_RISING`: Toggle the state on every rising `clk` crossing through `vth`.
- `P_DRIVE_OUT_LOW_WHEN_THE_STATE`: Drive `out` low when the state is low and to `vdd` when the state is high.
- `P_THE_FIRST_VALID_RISING_EDGE_DRIVES`: The first valid rising edge drives `out` high.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `divide_by_two_toggle.va`.
Do not add or omit artifacts.
