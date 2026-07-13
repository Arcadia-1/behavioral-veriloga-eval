# Trim Ctrl 5bit Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `trim_ctrl_5bit.va`: `trim_ctrl_5bit`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CONVERT_V_AIN_TO_THE_NEAREST`: Convert `V(ain)` to the nearest integer code using half-up rounding.
- `P_CLAMP_THE_CODE_TO_THE_VALID`: Clamp the code to the valid 5-bit trim range `0..31`.
- `P_DRIVE_DOUT0_DOUT4_FROM_THE_CLAMPED`: Drive `dout0..dout4` from the clamped binary code, LSB first.
- `P_DRIVE_HIGH_BITS_NEAR_VH_AND`: Drive high bits near `vh` and low bits near 0 V.
- `P_UPDATE_DETERMINISTICALLY_AS_THE_ANALOG_INPUT`: Update deterministically as the analog input changes.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `trim_ctrl_5bit.va`.
Every supplied `.va` file is editable; do not add or omit files.
