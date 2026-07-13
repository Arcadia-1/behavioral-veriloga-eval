# Trim Calibration Controller Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cdac_calibration.va`: `cdac_calibration`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_RESET`: trim initializes to 0.45 V and returns to 0.45 V on a rising clk edge while rst is high.
- `P_CLOCKED_STEP`: Each rising clk edge outside reset adds 0.06 V for high err and subtracts 0.06 V for low err.
- `P_TRIM_CLAMP`: trim is clamped to the inclusive 0.05 V to 0.85 V range.
- `P_CLOCKED_HOLD`: trim holds its state between rising clk updates.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cdac_calibration.va`.
Every supplied `.va` file is editable; do not add or omit files.
