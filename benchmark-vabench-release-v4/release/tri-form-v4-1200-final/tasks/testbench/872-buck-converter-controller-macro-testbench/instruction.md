# Buck Converter Controller Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Buck Converter Controller Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears PWM, duty metric, soft reference, and power-good.
- `P_SOFT_START_TRACKING`: At enabled rising clock edges soft_ref moves toward vref by the configured soft-step and never overshoots the target.
- `P_DUTY_DIRECTION_BOUNDS`: The duty metric increases when vfb is below soft_ref, decreases otherwise, and remains within the configured duty bounds.
- `P_PWM_ENCODING`: PWM high samples are rail-valid and their enabled-cycle activity is consistent with a nonzero bounded duty command.
- `P_POWER_GOOD_QUALIFICATION`: Power-good asserts only after three consecutive enabled clock updates with vfb within pgood_tol of vref and clears when qualification is lost.

The required trace names are: `time`, `vfb`, `vref`, `clk`, `rst`, `enable`, `pwm`, `duty_metric`, `soft_ref`, `pgood`.

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
