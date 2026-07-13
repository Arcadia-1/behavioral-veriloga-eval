# Calibration Deadband Controller Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `calibration_deadband_controller.va`: `calibration_deadband_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_RESET_TARGET`: Out initializes to target and returns to target while rst is above vth; metric is low during reset.
- `P_POSITIVE_ERROR_STEP`: At a rising clock crossing with vin minus target greater than deadband, out increases by one step_size and metric goes high.
- `P_NEGATIVE_ERROR_STEP`: At a rising clock crossing with vin minus target less than negative deadband, out decreases by one step_size and metric goes high.
- `P_DEADBAND_HOLD`: At a rising clock crossing with signed error inside the inclusive deadband, out holds and metric remains low.
- `P_OUTPUT_CLAMP`: Repeated updates cannot drive out below vmin or above vmax.
- `P_BETWEEN_EDGE_HOLD`: Out state does not follow vin between rising clock crossings.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `calibration_deadband_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.
