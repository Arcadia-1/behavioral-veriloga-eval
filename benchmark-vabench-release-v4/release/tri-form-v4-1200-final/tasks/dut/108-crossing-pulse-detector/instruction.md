# Crossing Pulse Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `source_crossing_pulse_detector.va`: `source_crossing_pulse_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_CROSS_PULSE`: A rising sigin crossing through sigcrossing initiates a sigout pulse.
- `P_FALLING_CROSS_PULSE`: A falling sigin crossing through sigcrossing also initiates a sigout pulse.
- `P_PULSE_WIDTH`: After each qualifying crossing, the output target remains at vlogic_high for pulse_width before returning to vlogic_low.
- `P_LOW_BETWEEN_EVENTS`: Sigout returns to vlogic_low between sufficiently separated threshold crossings.
- `P_REPEATABLE_BIDIRECTIONAL_EVENTS`: Alternating rising and falling crossings each produce corresponding pulses rather than only the first event or one polarity.
- `P_TRANSITION_TIMING`: Sigout changes use tdel delay with trise and tfall smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `source_crossing_pulse_detector.va`.
Do not add or omit artifacts.
