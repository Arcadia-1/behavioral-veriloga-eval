# PFD Up Down State Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pfd_up_down_state.va`: `pfd_up_down_state`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DETECT_RISING_REF_AND_FB_CROSSINGS`: Detect rising `ref` and `fb` crossings at `vdd/2`.
- `P_MAINTAIN_AN_INTEGER_DETECTOR_STATE_BOUNDED`: Maintain an integer detector state bounded to `-1`, `0`, or `+1`.
- `P_A_RISING_REF_EDGE_INCREMENTS_THE`: A rising `ref` edge increments the state up to `+1`.
- `P_A_RISING_FB_EDGE_DECREMENTS_THE`: A rising `fb` edge decrements the state down to `-1`.
- `P_DRIVE_UP_HIGH_WHEN_THE_STATE`: Drive `up` high when the state is `+1`.
- `P_DRIVE_DOWN_HIGH_WHEN_THE_STATE`: Drive `down` high when the state is `-1`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pfd_up_down_state.va`.
Every supplied `.va` file is editable; do not add or omit files.
