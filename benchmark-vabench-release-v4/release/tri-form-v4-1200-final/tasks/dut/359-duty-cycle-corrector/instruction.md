# Duty-cycle Corrector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dcc_top.va`: `dcc_top`
- `duty_meter.va`: `duty_meter`
- `trim_controller.va`: `trim_controller`
- `delay_pair.va`: `delay_pair`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable clears trim, duty metric, lock, and output clock.
- `P_DUTY_MEASUREMENT`: The metric reports high-time fraction over each complete input-clock cycle.
- `P_TRIM_DIRECTION`: The trim code moves up below the target window and down above it, with rail saturation.
- `P_EDGE_DELAY`: Rising edges pass without intentional delay while falling edges receive the latched trim-code delay.
- `P_LOCK_QUALIFICATION`: Lock asserts after three consecutive measured cycles inside the target window.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dcc_top.va`, `duty_meter.va`, `trim_controller.va`, `delay_pair.va`.
Do not add or omit artifacts.
