# Common-mode Feedback Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cmfb_loop_top.va`: `cmfb_loop_top`
- `cm_sensor.va`: `cm_sensor`
- `trim_controller.va`: `trim_controller`
- `output_balancer.va`: `output_balancer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears trim and lock, reports zero residual error, and bypasses correction.
- `P_COMMON_MODE_ERROR`: The reported common-mode error equals the corrected output average minus vcm.
- `P_TRIM_DIRECTION`: At enabled rising clock edges the bounded unsigned trim code moves in the direction that reduces representable positive common-mode error.
- `P_DIFFERENTIAL_PRESERVATION`: Common-mode correction preserves input differential polarity and differential magnitude unless a supply clamp is reached.
- `P_LOCK_QUALIFICATION`: Lock asserts only after two consecutive enabled updates within lock_tol.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cmfb_loop_top.va`, `cm_sensor.va`, `trim_controller.va`, `output_balancer.va`.
Every supplied `.va` file is editable; do not add or omit files.
