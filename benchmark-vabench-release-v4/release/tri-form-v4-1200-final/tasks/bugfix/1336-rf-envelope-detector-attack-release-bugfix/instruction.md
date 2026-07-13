# RF Envelope Detector with Attack/Release Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `rf_envelope_detector_attack_release.va`: `rf_envelope_detector_attack_release`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear envelope, metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, estimate input magnitude as distance from `vcm`.
- `P_USE_A_FASTER_ATTACK_STEP_WHEN`: Use a faster attack step when magnitude rises and a slower release step when it falls.
- `P_DRIVE_ENVELOPE_WITH_THE_TRACKED_MAGNITUDE`: Drive `envelope` with the tracked magnitude mapped into the public voltage range.
- `P_EXPOSE_WHETHER_THE_LAST_UPDATE_USED`: Expose whether the last update used attack or release on `attack_metric`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `rf_envelope_detector_attack_release.va`.
Every supplied `.va` file is editable; do not add or omit files.
