# Crossing Pulse Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `source_crossing_pulse_detector.va`: `source_crossing_pulse_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_CROSS_PULSE`: A rising sigin crossing through sigcrossing initiates a sigout pulse.
- `P_FALLING_CROSS_PULSE`: A falling sigin crossing through sigcrossing also initiates a sigout pulse.
- `P_PULSE_WIDTH`: After each qualifying crossing, the output target remains at vlogic_high for pulse_width before returning to vlogic_low.
- `P_LOW_BETWEEN_EVENTS`: Sigout returns to vlogic_low between sufficiently separated threshold crossings.
- `P_REPEATABLE_BIDIRECTIONAL_EVENTS`: Alternating rising and falling crossings each produce corresponding pulses rather than only the first event or one polarity.
- `P_TRANSITION_TIMING`: Sigout changes use tdel delay with trise and tfall smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `source_crossing_pulse_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
