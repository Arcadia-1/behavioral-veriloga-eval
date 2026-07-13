# Decision Router Logic

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `decision_router_logic.va`: `decision_router_logic`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INTERPRET_VIN1_VIN2_AND_VALID_RELATIVE`: Interpret `vin1`, `vin2`, and `valid` relative to `vth`; all routed decisions below are evaluated from those voltage-coded Boolean inputs.
- `P_DRIVE_DM_HIGH_WHEN_VIN1_IS`: Drive `dm` high when `vin1` is high and low otherwise.
- `P_DRIVE_DL_HIGH_WHEN_VIN1_IS`: Drive `dl` high when `vin1` is low and `vin2` is high, and low otherwise.
- `P_DRIVE_X_HIGH_WHEN_VALID_IS`: Drive `x` high only when `valid` is high and both decision inputs are low.
- `P_DRIVE_Y_HIGH_WHEN_VALID_IS`: Drive `y` high only when `valid` is high and both decision inputs are high.
- `P_DRIVE_Z_HIGH_WHEN_VALID_IS`: Drive `z` high only when `valid` is high, `vin1` is low, and `vin2` is high.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `decision_router_logic.va`.
Do not add or omit artifacts.
