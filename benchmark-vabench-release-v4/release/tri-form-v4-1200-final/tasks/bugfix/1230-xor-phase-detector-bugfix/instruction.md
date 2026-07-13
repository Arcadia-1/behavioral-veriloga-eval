# XOR Phase Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `xor_phase_detector.va`: `xor_phase_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INTERPRET_REF_AND_FB_LOGIC_LEVELS`: Interpret `ref` and `fb` logic levels using a threshold of `vdd/2`.
- `P_DRIVE_UP_HIGH_WHEN_THE_INTERPRETED`: Drive `up` high when the interpreted `ref` and `fb` levels differ.
- `P_DRIVE_DOWN_HIGH_WHEN_THE_INTERPRETED`: Drive `down` high when the interpreted `ref` and `fb` levels match.
- `P_UPDATE_OUTPUTS_COMBINATIONALLY_FROM_THE_CURREN`: Update outputs combinationally from the current input voltages.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `xor_phase_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
