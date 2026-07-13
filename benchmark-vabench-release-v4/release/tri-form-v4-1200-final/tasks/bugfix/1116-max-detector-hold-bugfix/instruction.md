# Max Detector Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `max_detector_hold.va`: `max_detector_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_INPUT`: At simulation start, the held output is initialized from the input rather than from a fixed rail.
- `P_CAPTURE_NEW_MAX`: Whenever vin exceeds every previously observed value, vout updates to that new maximum.
- `P_HOLD_ON_FALL`: When vin falls below the held maximum, vout retains the previously captured maximum.
- `P_MONOTONE_OUTPUT`: Across transient operation, vout is monotone nondecreasing.
- `P_RUNNING_MAX`: At each observation time, vout equals the maximum vin value observed from simulation start through that time.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `max_detector_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.
