# Decision Router Logic Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `decision_router_logic.va`: `decision_router_logic`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INTERPRET_VIN1_VIN2_AND_VALID_RELATIVE`: Interpret `vin1`, `vin2`, and `valid` relative to `vth`; all routed decisions below are evaluated from those voltage-coded Boolean inputs.
- `P_DRIVE_DM_HIGH_WHEN_VIN1_IS`: Drive `dm` high when `vin1` is high and low otherwise.
- `P_DRIVE_DL_HIGH_WHEN_VIN1_IS`: Drive `dl` high when `vin1` is low and `vin2` is high, and low otherwise.
- `P_DRIVE_X_HIGH_WHEN_VALID_IS`: Drive `x` high only when `valid` is high and both decision inputs are low.
- `P_DRIVE_Y_HIGH_WHEN_VALID_IS`: Drive `y` high only when `valid` is high and both decision inputs are high.
- `P_DRIVE_Z_HIGH_WHEN_VALID_IS`: Drive `z` high only when `valid` is high, `vin1` is low, and `vin2` is high.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `decision_router_logic.va`.
Every supplied `.va` file is editable; do not add or omit files.
