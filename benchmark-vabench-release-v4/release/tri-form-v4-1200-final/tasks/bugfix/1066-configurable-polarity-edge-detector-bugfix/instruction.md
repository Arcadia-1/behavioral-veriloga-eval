# Configurable Polarity Edge Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `configurable_polarity_edge_detector.va`: `configurable_polarity_edge_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_SELECTION`: When rise_en is above vth, each rising crossing of sig through vth produces one output pulse.
- `P_FALLING_SELECTION`: When rise_en is below vth, each falling crossing of sig through vth produces one output pulse.
- `P_OPPOSITE_EDGE_REJECTION`: An edge opposite to the polarity selected by rise_en does not produce a pulse.
- `P_BOUNDED_PULSE`: Each detected edge produces a bounded short pulse with nominal width about 2 ns rather than a latched high level.
- `P_OUTPUT_LEVELS`: pulse uses 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `configurable_polarity_edge_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
