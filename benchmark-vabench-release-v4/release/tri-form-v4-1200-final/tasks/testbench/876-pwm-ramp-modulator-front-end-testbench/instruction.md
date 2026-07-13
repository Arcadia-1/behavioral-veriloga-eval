# PWM Ramp Modulator Front-end Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PWM Ramp Modulator Front-end` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_RESET_OR_A_LOW_ENABLE_CLEARS`: Reset or a low `enable` clears the ramp, PWM output, cycle marker, and duty metric.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, advance `ramp_out` by `ramp_step` and wrap to `vss` at full scale.
- `P_CYCLE_START_PULSES_HIGH_FOR_THE`: `cycle_start` pulses high for the clock edge where the ramp wraps.
- `P_PWM_OUT_IS_HIGH_WHEN_VCTRL`: `pwm_out` is high when `vctrl` is greater than the current ramp value and low otherwise.
- `P_DUTY_METRIC_TRACKS_THE_CLIPPED_DUTY`: `duty_metric` tracks the clipped duty command between `vss` and `vdd`.

The required trace names are: `time`, `clk`, `rst`, `enable`, `vctrl`, `ramp_out`, `pwm_out`, `cycle_start`, `duty_metric`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
