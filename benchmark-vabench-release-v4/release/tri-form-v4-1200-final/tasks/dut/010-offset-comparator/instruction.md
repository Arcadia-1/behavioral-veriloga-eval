# Offset Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cmp_offset_ref.va`: `cmp_offset_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_SAMPLE`: OUT_P updates only on CLK rising crossings through the local rail midpoint.
- `P_OFFSET_DECISION`: OUT_P latches high only when VINP relative to VINN is greater than the positive vos threshold.
- `P_LATCH_HOLD`: OUT_P holds its sampled decision between rising clock edges.
- `P_RAIL_REFERENCE`: OUT_P low and high levels track VSS and VDD respectively with finite smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cmp_offset_ref.va`.
Do not add or omit artifacts.
