# Trim Calibration Controller

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cdac_calibration.va`: `cdac_calibration`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_RESET`: trim initializes to 0.45 V and returns to 0.45 V on a rising clk edge while rst is high.
- `P_CLOCKED_STEP`: Each rising clk edge outside reset adds 0.06 V for high err and subtracts 0.06 V for low err.
- `P_TRIM_CLAMP`: trim is clamped to the inclusive 0.05 V to 0.85 V range.
- `P_CLOCKED_HOLD`: trim holds its state between rising clk updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cdac_calibration.va`.
Do not add or omit artifacts.
