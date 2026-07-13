# Current-limited Regulator Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `current_limited_regulator_macro.va`: `current_limited_regulator_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation drives vout, limit_metric, and regulation_ok low.
- `P_NORMAL_REGULATION`: With adequate headroom and sub-limit demand, vout equals vref and regulation_ok is asserted.
- `P_DROPOUT_CLAMP`: When input headroom is insufficient, vout is clamped to max(vss, vin minus dropout).
- `P_CURRENT_LIMITING`: Demand above demand_limit produces limit_metric equal to the overload and reduces vout by that overload subject to rails and dropout.
- `P_REGULATION_FLAG`: regulation_ok is high only for enabled, non-reset, non-limited operation with enough input headroom.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `current_limited_regulator_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
