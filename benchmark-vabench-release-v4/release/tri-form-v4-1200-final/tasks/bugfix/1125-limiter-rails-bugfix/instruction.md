# Limiter Rails Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `limiter_rails.va`: `limiter_rails`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RAIL_DERIVED_LIMITS`: Derive the upper limit as `V(vdd) - V(vmax)` and the lower limit as `V(vss) + V(vmin)`.
- `P_PASS_WITHIN_LIMITS`: When `V(vin)` lies between the derived limits, drive `vout` to `V(vin)`.
- `P_LIMIT_ABOVE_UPPER`: When `V(vin)` exceeds the upper limit, drive `vout` to the upper limit.
- `P_LIMIT_BELOW_LOWER`: When `V(vin)` is below the lower limit, drive `vout` to the lower limit.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `limiter_rails.va`.
Every supplied `.va` file is editable; do not add or omit files.
