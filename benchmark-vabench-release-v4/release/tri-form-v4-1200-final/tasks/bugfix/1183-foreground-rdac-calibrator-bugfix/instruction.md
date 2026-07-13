# Foreground RDAC Calibrator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `foreground_rdac_calibrator.va`: `foreground_rdac_calibrator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_MSB_TRIAL_CODE`: At startup, calibration is active with `dc6` asserted and all lower RDAC bits deasserted.
- `P_CLOCKED_RDAC_DECISION_SEQUENCE`: On each rising `ck` crossing while active, resolve the current trial bit from `d` versus `vth` and advance from MSB to LSB.
- `P_DECISION_POLARITY`: Comparator-low and comparator-high decisions update the trial bit in the declared polarity without inverting the search direction.
- `P_CALIBRATION_COMPLETION`: After the final RDAC decision, deassert calibration enable and hold the completed code.
- `P_RDAC_OUTPUT_LEVELS`: All RDAC code and enable outputs remain voltage-coded at valid low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `foreground_rdac_calibrator.va`.
Every supplied `.va` file is editable; do not add or omit files.
