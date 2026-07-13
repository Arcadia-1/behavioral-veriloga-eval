# PWM Ramp Modulator Front-end

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pwm_ramp_modulator.va`: `pwm_ramp_modulator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_OR_A_LOW_ENABLE_CLEARS`: Reset or a low `enable` clears the ramp, PWM output, cycle marker, and duty metric.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, advance `ramp_out` by `ramp_step` and wrap to `vss` at full scale.
- `P_CYCLE_START_PULSES_HIGH_FOR_THE`: `cycle_start` pulses high for the clock edge where the ramp wraps.
- `P_PWM_OUT_IS_HIGH_WHEN_VCTRL`: `pwm_out` is high when `vctrl` is greater than the current ramp value and low otherwise.
- `P_DUTY_METRIC_TRACKS_THE_CLIPPED_DUTY`: `duty_metric` tracks the clipped duty command between `vss` and `vdd`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pwm_ramp_modulator.va`.
Do not add or omit artifacts.
