# Comparator Offset Search

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `comparator_offset_search_ref.va`: `comparator_offset_search_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_MEASUREMENT_STATE`: Before the first positive threshold crossing, valid, trip_v, and offset_est remain in the zero-measurement state.
- `P_DECISION_THRESHOLD`: Outp is high when V(inp,vss)-V(inn,vss) is above vos and low after that differential falls below vos.
- `P_FIRST_POSITIVE_CAPTURE`: The first positive crossing of the vos threshold captures the input trip voltage and measured differential offset and asserts valid.
- `P_CAPTURE_HOLD`: After valid asserts, trip_v, offset_est, and valid retain their first-measurement values despite later differential-input changes.
- `P_RAIL_REFERENCED_LOGIC`: Outp and valid use the vdd-to-vss logic range with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `comparator_offset_search_ref.va`.
Do not add or omit artifacts.
