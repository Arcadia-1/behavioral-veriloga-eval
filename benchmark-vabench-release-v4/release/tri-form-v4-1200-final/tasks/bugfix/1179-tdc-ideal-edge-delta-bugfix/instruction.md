# TDC Ideal Edge Delta Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `tdc_ideal_edge_delta.va`: `tdc_ideal_edge_delta`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAMPLE_REARMS_MEASUREMENT`: At initialization and each rising `samp` crossing, input trigger flags clear while the previous output is retained until a new edge pair is measured.
- `P_INPUT_EDGE_PAIR_CAPTURE`: A measurement completes only after the required `inp` and `inn` rising-edge pair has been observed.
- `P_SIGNED_DELTA_POLARITY`: `vout` represents the `inp` minus `inn` edge-time delta with the specified polarity.
- `P_FULL_RANGE_SCALE`: The reported timing delta uses the specified full-range scale rather than a half-range or alternate denominator.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `tdc_ideal_edge_delta.va`.
Every supplied `.va` file is editable; do not add or omit files.
