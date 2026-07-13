# Comparator Offset Search Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `comparator_offset_search_ref.va`: `comparator_offset_search_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_MEASUREMENT_STATE`: Before the first positive threshold crossing, valid, trip_v, and offset_est remain in the zero-measurement state.
- `P_DECISION_THRESHOLD`: Outp is high when V(inp,vss)-V(inn,vss) is above vos and low after that differential falls below vos.
- `P_FIRST_POSITIVE_CAPTURE`: The first positive crossing of the vos threshold captures the input trip voltage and measured differential offset and asserts valid.
- `P_CAPTURE_HOLD`: After valid asserts, trip_v, offset_est, and valid retain their first-measurement values despite later differential-input changes.
- `P_RAIL_REFERENCED_LOGIC`: Outp and valid use the vdd-to-vss logic range with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `comparator_offset_search_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
