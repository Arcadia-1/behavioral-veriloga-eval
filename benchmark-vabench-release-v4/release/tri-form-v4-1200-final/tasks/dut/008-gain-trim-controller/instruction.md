# Gain Trim Controller

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `gain_trim_controller.va`: `gain_trim_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_RESET`: gain_ctrl initializes to 0.30 V and returns to 0.30 V on a rising clk edge while rst is high.
- `P_ERROR_DIRECTION`: On rising clk edges, gain_ctrl increases by 0.05 V below target-0.02 V and decreases by 0.05 V above target+0.02 V.
- `P_DEADBAND_HOLD`: gain_ctrl holds when meas is within the inclusive target deadband.
- `P_CONTROL_CLAMP`: gain_ctrl remains within the inclusive 0.05 V to 0.85 V range.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `gain_trim_controller.va`.
Do not add or omit artifacts.
