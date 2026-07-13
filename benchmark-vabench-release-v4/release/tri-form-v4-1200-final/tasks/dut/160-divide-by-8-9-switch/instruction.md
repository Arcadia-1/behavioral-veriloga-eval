# Divide By 8 9 Switch

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `divide_by_8_9_switch.va`: `divide_by_8_9_switch`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MODULUS_SWITCHING_ON_MC_EDGES`: `mc` crossings switch the divider between divide-by-8 and divide-by-9 operation and can restore divide-by-8 after divide-by-9.
- `P_DIVIDER_DUTY_WINDOW`: The divider output high window spans the specified count interval for the active modulus.
- `P_OUTPUT_RAIL_LEVEL`: `out` uses the declared high and low output levels without amplitude scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `divide_by_8_9_switch.va`.
Do not add or omit artifacts.
