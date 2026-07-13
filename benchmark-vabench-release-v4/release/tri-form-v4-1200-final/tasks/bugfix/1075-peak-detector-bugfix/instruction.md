# Peak Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `peak_detector.va`: `peak_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_ZERO`: The retained peak and vout initialize to 0 V.
- `P_SAMPLED_MEASUREMENT`: When reset is inactive, vin is considered for peak updates at periodic 500 ps sample instants.
- `P_MAX_RETENTION`: At each sample, a vin value above the retained peak replaces it; lower or equal samples leave vout unchanged.
- `P_MONOTONIC_HOLD`: Between resets, the retained peak does not decrease and remains held between sample instants.
- `P_RESET_CLEAR`: While rst is above vth, the retained peak is cleared and vout returns to 0 V.
- `P_OUTPUT_SMOOTHING`: Changes of the retained peak appear on vout with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `peak_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
