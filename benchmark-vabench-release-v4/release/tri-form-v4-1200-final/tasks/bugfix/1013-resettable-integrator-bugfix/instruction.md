# Resettable Integrator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `resettable_integrator.va`: `resettable_integrator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_ZERO`: vout begins at 0 V.
- `P_TIMER_INTEGRATION`: While reset is low, each dt timer event adds gain*vin*dt to the accumulator.
- `P_ACTIVE_HIGH_RESET`: When rst is above vth at a timer event, the accumulator and vout return toward 0 V and later restart from zero.
- `P_ACCUMULATOR_CLAMP`: vout remains in the closed 0 V to vmax range.
- `P_EVENT_HOLD`: The accumulated state changes only on dt timer events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `resettable_integrator.va`.
Every supplied `.va` file is editable; do not add or omit files.
