# Capacitive Weighted SAR Feedback DAC

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cdac_cal.va`: `cdac_cal`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_HOLD`: The DAC samples code and calibration inputs on rising CLK edges and holds the resulting output between edges.
- `P_CODE_MONOTONICITY`: Increasing effective code increases VDAC_P minus VDAC_N.
- `P_CALIBRATION_WEIGHT`: CAL0 contributes one calibration unit, CAL1 contributes two, and each unit offsets the main code by 32 codes.
- `P_DIFFERENTIAL_COMMON_MODE`: VDAC_P and VDAC_N are complementary about vcm.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cdac_cal.va`.
Do not add or omit artifacts.
