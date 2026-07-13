# Safe Voltage Divider Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `safe_voltage_divider.va`: `safe_voltage_divider`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_GAINED_DIVISION`: Drive `sigout` to `gain * V(signumer) / guarded_denominator`.
- `P_DENOMINATOR_MAGNITUDE_FLOOR`: When `abs(V(sigdenom)) < min_sigdenom`, use a denominator magnitude of `min_sigdenom`.
- `P_DENOMINATOR_SIGN_PRESERVED`: Preserve the original denominator sign when applying the minimum denominator guard.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `safe_voltage_divider.va`.
Every supplied `.va` file is editable; do not add or omit files.
