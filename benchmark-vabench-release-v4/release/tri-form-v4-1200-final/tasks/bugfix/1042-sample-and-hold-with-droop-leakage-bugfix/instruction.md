# Sample And Hold With Droop Leakage Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `leaky_hold.va`: `leaky_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAMPLE_CAPTURE`: Each rising sample crossing while reset is inactive captures the instantaneous vin voltage into the held state.
- `P_HOLD_BETWEEN_EVENTS`: Between sample and leakage events, vout reflects the retained held state rather than continuously tracking vin.
- `P_PERIODIC_DROOP`: At every leak_period update while reset is inactive, the held value is multiplied by decay.
- `P_RESET_CLEAR`: Active reset clears the held state to 0 V at sampling or leakage update events.
- `P_SMOOTH_OUTPUT`: Vout approaches each held-state target with the finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `leaky_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.
