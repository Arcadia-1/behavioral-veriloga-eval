# Buck Converter Controller Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `buck_ctrl_top.va`: `buck_ctrl_top`
- `error_comparator.va`: `error_comparator`
- `power_good.va`: `power_good`
- `pwm_modulator.va`: `pwm_modulator`
- `soft_start.va`: `soft_start`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears PWM, duty metric, soft reference, and power-good.
- `P_SOFT_START_TRACKING`: At enabled rising clock edges soft_ref moves toward vref by the configured soft-step and never overshoots the target.
- `P_DUTY_DIRECTION_BOUNDS`: The duty metric increases when vfb is below soft_ref, decreases otherwise, and remains within the configured duty bounds.
- `P_PWM_ENCODING`: PWM high samples are rail-valid and their enabled-cycle activity is consistent with a nonzero bounded duty command.
- `P_POWER_GOOD_QUALIFICATION`: Power-good asserts only after three consecutive enabled clock updates with vfb within pgood_tol of vref and clears when qualification is lost.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `buck_ctrl_top.va`, `error_comparator.va`, `power_good.va`, `pwm_modulator.va`, `soft_start.va`.
Do not add or omit artifacts.
