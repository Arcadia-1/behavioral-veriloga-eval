# PWM Ramp Modulator Front-end Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pwm_ramp_modulator.va`: `pwm_ramp_modulator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_A_LOW_ENABLE_CLEARS`: Reset or a low `enable` clears the ramp, PWM output, cycle marker, and duty metric.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, advance `ramp_out` by `ramp_step` and wrap to `vss` at full scale.
- `P_CYCLE_START_PULSES_HIGH_FOR_THE`: `cycle_start` pulses high for the clock edge where the ramp wraps.
- `P_PWM_OUT_IS_HIGH_WHEN_VCTRL`: `pwm_out` is high when `vctrl` is greater than the current ramp value and low otherwise.
- `P_DUTY_METRIC_TRACKS_THE_CLIPPED_DUTY`: `duty_metric` tracks the clipped duty command between `vss` and `vdd`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pwm_ramp_modulator.va`.
Every supplied `.va` file is editable; do not add or omit files.
