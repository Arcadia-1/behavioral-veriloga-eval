# Phase Detector Chopper Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `phase_detector_chopper.va`: `phase_detector_chopper`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_POSITIVE_LO_GAIN_PATH`: When `vlocal_osc` is positive, drive `vif = gain * vin_rf`.
- `P_NEGATIVE_LO_CHOP_PATH`: When `vlocal_osc` is not positive, drive `vif = -gain * vin_rf`.
- `P_CONTINUOUS_TRACKING`: `vif` tracks `vin_rf` and `vlocal_osc` continuously without clocked state or hidden latching.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `phase_detector_chopper.va`.
Every supplied `.va` file is editable; do not add or omit files.
