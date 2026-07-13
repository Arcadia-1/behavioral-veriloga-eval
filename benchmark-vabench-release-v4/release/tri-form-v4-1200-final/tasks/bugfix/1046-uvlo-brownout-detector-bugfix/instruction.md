# UVLO Brownout Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `uvlo_brownout_detector.va`: `uvlo_brownout_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_FAULT`: Active reset clears the power-good out signal and drives metric to the public fault code 0.9 V.
- `P_UPPER_TRIP_ASSERT`: On a sampled update, vin strictly greater than 0.65 V asserts power-good out.
- `P_HYSTERESIS_HOLD`: For sampled vin values from 0.55 V through 0.65 V inclusive, out preserves its previous power-good state.
- `P_BROWNOUT_CLEAR`: On a sampled update, vin strictly less than 0.55 V clears out to the brownout state.
- `P_STATUS_DISTINCTION`: Metric is the checker-observable status code: 0.1 V when out is power-good high and 0.9 V when reset, undervoltage, or brownout is active.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `uvlo_brownout_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
