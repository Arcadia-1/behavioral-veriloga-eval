# RS Latch Voltage

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `rs_latch_voltage.va`: `rs_latch_voltage`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_LOGIC_THRESHOLDS_OUTPUT_AMPLITUDE`: Interpret set and reset as logic high above 0.45 V and drive outputs with 0.9 V high and 0.0 V low levels.
- `P_SET_RESET_PRIORITY`: A set-only input drives Q high, and a reset-only input drives Q low.
- `P_HOLD_STATE`: When neither set-only nor reset-only is asserted, preserve the previous Q state after initializing Q low.
- `P_QBAR_COMPLEMENT`: Drive `vout_qbar` as the logical complement of Q.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `rs_latch_voltage.va`.
Do not add or omit artifacts.
