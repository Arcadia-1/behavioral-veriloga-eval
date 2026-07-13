# Slew Rate Limiter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `slew_rate_limiter.va`: `slew_rate_limiter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_ZERO`: vout begins at 0 V.
- `P_PERIODIC_UPDATE`: The state changes only on the public 1 ns periodic update schedule.
- `P_BIDIRECTIONAL_STEP_LIMIT`: Each rising or falling update changes the state toward vin by no more than step.
- `P_NEAR_TARGET_SETTLE`: When vin is within one step, vout may settle directly to vin.
- `P_EVENTUAL_TRACKING`: The limited response eventually reaches sustained high and low input levels while remaining non-instantaneous.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `slew_rate_limiter.va`.
Every supplied `.va` file is editable; do not add or omit files.
