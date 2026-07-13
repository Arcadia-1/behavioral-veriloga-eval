# Ramp Step Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bound_step_period_guard_ref.va`: `bound_step_period_guard_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PHASE_RAMP`: Within each period, phase_out rises linearly from VSS toward VDD as normalized phase advances from zero toward one.
- `P_PHASE_WRAP`: At each period boundary, phase_out wraps from the end of the ramp back to VSS and begins the next ramp.
- `P_GUARD_WINDOW`: guard_out is at VDD during the first min(pulse_w, period) seconds of each period.
- `P_GUARD_LOW`: If pulse_w is less than period, guard_out remains at VSS after the guard window and before the next period boundary; if pulse_w is greater than or equal to period, guard_out has no low remainder in that period.
- `P_RAIL_TRACKING`: Both outputs derive their low and high endpoints from the observed VSS and VDD rails rather than fixed absolute voltages.
- `P_PERIODICITY`: The ramp-wrap and guard-window pattern repeats every period with guard transitions smoothed by tedge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bound_step_period_guard_ref.va`.
Do not add or omit artifacts.
