# Gain Trim Controller Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `gain_trim_controller.va`: `gain_trim_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_RESET`: gain_ctrl initializes to 0.30 V and returns to 0.30 V on a rising clk edge while rst is high.
- `P_ERROR_DIRECTION`: On rising clk edges, gain_ctrl increases by 0.05 V below target-0.02 V and decreases by 0.05 V above target+0.02 V.
- `P_DEADBAND_HOLD`: gain_ctrl holds when meas is within the inclusive target deadband.
- `P_CONTROL_CLAMP`: gain_ctrl remains within the inclusive 0.05 V to 0.85 V range.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `gain_trim_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.
