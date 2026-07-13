# Dual Track Sample Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dual_track_sample_hold.va`: `dual_track_sample_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_COMPLEMENTARY_TRACK_HOLD_SEQUENCE`: During low clock phase the input stage tracks `vin` while output holds; after the rising edge, the output stage tracks the retained input-stage value during high clock phase; after the falling edge, output holds until the next high phase.
- `P_FINITE_TRACKING_AND_HOLD`: Use finite acquisition updates and preserve held values between tracking windows rather than making the output continuously transparent or a single ideal edge sample.
- `P_PHASE_MONITOR_POLARITY`: Drive `phase` high only during output-stage tracking and low otherwise.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dual_track_sample_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.
