# Bin2ther 2b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bin2ther_2b.va`: `bin2ther_2b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INTERPRET_B1_AND_B0_RELATIVE_TO`: Interpret `b1` and `b0` relative to the local rail midpoint.
- `P_DRIVE_T0_AND_T1_HIGH_TOGETHER`: Drive `t0` and `t1` high together when `b1` is high.
- `P_DRIVE_T2_HIGH_WHEN_B0_IS`: Drive `t2` high when `b0` is high.
- `P_DRIVE_EACH_LOW_OUTPUT_TO_THE`: Drive each low output to the local `gnd` rail and each high output to the local `vdd` rail.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bin2ther_2b.va`.
Do not add or omit artifacts.
