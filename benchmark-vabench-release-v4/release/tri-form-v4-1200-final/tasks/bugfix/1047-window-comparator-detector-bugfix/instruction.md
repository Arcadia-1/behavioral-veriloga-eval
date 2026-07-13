# Window Comparator Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `window_comparator_ref.va`: `window_comparator_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_WINDOW_STATE`: At initialization, out reflects whether vin relative to VSS lies strictly between vlow and vhigh.
- `P_INSIDE_WINDOW_HIGH`: Out is at the VDD rail only while vlow < V(vin,VSS) < vhigh.
- `P_BOUNDARY_EXCLUSION`: Out is at the VSS rail when V(vin,VSS) is equal to or outside either window boundary.
- `P_BIDIRECTIONAL_CROSSINGS`: Crossings of both vlow and vhigh in either direction update the retained in-window decision.
- `P_RAIL_SMOOTHING`: Out is rail-referenced to VDD and VSS with finite transition smoothing set by tedge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `window_comparator_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
