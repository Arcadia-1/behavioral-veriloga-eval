# Ramp Step Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bound_step_period_guard_ref.va`: `bound_step_period_guard_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PHASE_RAMP`: Within each period, phase_out rises linearly from VSS toward VDD as normalized phase advances from zero toward one.
- `P_PHASE_WRAP`: At each period boundary, phase_out wraps from the end of the ramp back to VSS and begins the next ramp.
- `P_GUARD_WINDOW`: guard_out is at VDD during the first min(pulse_w, period) seconds of each period.
- `P_GUARD_LOW`: If pulse_w is less than period, guard_out remains at VSS after the guard window and before the next period boundary; if pulse_w is greater than or equal to period, guard_out has no low remainder in that period.
- `P_RAIL_TRACKING`: Both outputs derive their low and high endpoints from the observed VSS and VDD rails rather than fixed absolute voltages.
- `P_PERIODICITY`: The ramp-wrap and guard-window pattern repeats every period with guard transitions smoothed by tedge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bound_step_period_guard_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
