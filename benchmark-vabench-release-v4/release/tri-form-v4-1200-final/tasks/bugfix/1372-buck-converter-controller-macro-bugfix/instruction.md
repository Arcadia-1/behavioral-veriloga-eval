# Buck Converter Controller Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `buck_ctrl_top.va`: `buck_ctrl_top`
- `error_comparator.va`: `error_comparator`
- `power_good.va`: `power_good`
- `pwm_modulator.va`: `pwm_modulator`
- `soft_start.va`: `soft_start`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears PWM, duty metric, soft reference, and power-good.
- `P_SOFT_START_TRACKING`: At enabled rising clock edges soft_ref moves toward vref by the configured soft-step and never overshoots the target.
- `P_DUTY_DIRECTION_BOUNDS`: The duty metric increases when vfb is below soft_ref, decreases otherwise, and remains within the configured duty bounds.
- `P_PWM_ENCODING`: PWM high samples are rail-valid and their enabled-cycle activity is consistent with a nonzero bounded duty command.
- `P_POWER_GOOD_QUALIFICATION`: Power-good asserts only after three consecutive enabled clock updates with vfb within pgood_tol of vref and clears when qualification is lost.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `buck_ctrl_top.va`, `error_comparator.va`, `power_good.va`, `pwm_modulator.va`, `soft_start.va`.
Every supplied `.va` file is editable; do not add or omit files.
