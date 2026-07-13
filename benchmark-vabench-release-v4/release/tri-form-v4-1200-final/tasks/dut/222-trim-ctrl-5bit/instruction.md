# Trim Ctrl 5bit

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `trim_ctrl_5bit.va`: `trim_ctrl_5bit`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CONVERT_V_AIN_TO_THE_NEAREST`: Convert `V(ain)` to the nearest integer code using half-up rounding.
- `P_CLAMP_THE_CODE_TO_THE_VALID`: Clamp the code to the valid 5-bit trim range `0..31`.
- `P_DRIVE_DOUT0_DOUT4_FROM_THE_CLAMPED`: Drive `dout0..dout4` from the clamped binary code, LSB first.
- `P_DRIVE_HIGH_BITS_NEAR_VH_AND`: Drive high bits near `vh` and low bits near 0 V.
- `P_UPDATE_DETERMINISTICALLY_AS_THE_ANALOG_INPUT`: Update deterministically as the analog input changes.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `trim_ctrl_5bit.va`.
Do not add or omit artifacts.
