# Calibration Deadband Controller

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `calibration_deadband_controller.va`: `calibration_deadband_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_RESET_TARGET`: Out initializes to target and returns to target while rst is above vth; metric is low during reset.
- `P_POSITIVE_ERROR_STEP`: At a rising clock crossing with vin minus target greater than deadband, out increases by one step_size and metric goes high.
- `P_NEGATIVE_ERROR_STEP`: At a rising clock crossing with vin minus target less than negative deadband, out decreases by one step_size and metric goes high.
- `P_DEADBAND_HOLD`: At a rising clock crossing with signed error inside the inclusive deadband, out holds and metric remains low.
- `P_OUTPUT_CLAMP`: Repeated updates cannot drive out below vmin or above vmax.
- `P_BETWEEN_EDGE_HOLD`: Out state does not follow vin between rising clock crossings.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `calibration_deadband_controller.va`.
Do not add or omit artifacts.
