# RS Phase Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `rs_phase_detector.va`: `rs_phase_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DETECT_RISING_REF_AND_FB_CROSSINGS`: Detect rising `ref` and `fb` crossings at `vdd/2`.
- `P_A_RISING_REF_EDGE_SETS_THE`: A rising `ref` edge sets the latch state so `up` is high and `down` is low.
- `P_A_RISING_FB_EDGE_RESETS_THE`: A rising `fb` edge resets the latch state so `up` is low and `down` is high.
- `P_HOLD_THE_MOST_RECENT_LATCH_STATE`: Hold the most recent latch state between qualifying input edges.
- `P_INITIALIZE_TO_THE_RESET_STATE_WITH`: Initialize to the reset state with `up` low and `down` high.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `rs_phase_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
