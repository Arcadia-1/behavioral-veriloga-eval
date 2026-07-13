# Offset Comparator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cmp_offset_ref.va`: `cmp_offset_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_SAMPLE`: OUT_P updates only on CLK rising crossings through the local rail midpoint.
- `P_OFFSET_DECISION`: OUT_P latches high only when VINP relative to VINN is greater than the positive vos threshold.
- `P_LATCH_HOLD`: OUT_P holds its sampled decision between rising clock edges.
- `P_RAIL_REFERENCE`: OUT_P low and high levels track VSS and VDD respectively with finite smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cmp_offset_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
