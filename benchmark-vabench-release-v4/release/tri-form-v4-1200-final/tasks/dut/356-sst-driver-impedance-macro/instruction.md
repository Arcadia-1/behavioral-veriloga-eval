# SST Driver Impedance Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sst_driver_macro.va`: `sst_driver_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable drives common mode and clears public metrics.
- `P_CLOCKED_DATA`: The data decision updates only on enabled rising clock edges.
- `P_SWING_MAPPING`: The trim code selects swing_min plus swing_lsb per code step.
- `P_DATA_POLARITY`: High and low latched data drive equal-polarity swings around VCM.
- `P_TRIM_METRIC`: The trim metric maps unsigned codes 0 and 7 to the public rails linearly.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sst_driver_macro.va`.
Do not add or omit artifacts.
