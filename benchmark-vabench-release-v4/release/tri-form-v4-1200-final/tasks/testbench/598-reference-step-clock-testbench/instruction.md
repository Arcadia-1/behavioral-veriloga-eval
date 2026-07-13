# Reference Step Clock Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Reference Step Clock` DUT. The evaluator runs the same submitted bytes
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

- `P_SUPPLY_REFERENCED_RAILS`: CLK low and high levels track VSS and VDD respectively.
- `P_PRE_SWITCH_PERIOD`: Clock cycles before t_switch have full period period_pre.
- `P_POST_SWITCH_PERIOD`: Clock cycles scheduled after t_switch have full period period_post.
- `P_CADENCE_STEP`: The waveform changes cadence near t_switch without stopping, duplicating, or losing clock transitions.
- `P_HALF_DUTY_CYCLE`: CLK duty cycle remains close to 50 percent on both sides of the cadence step.
- `P_PARAMETERIZED_TIMING`: Nearby legal overrides of period_pre, period_post, t_switch, and tedge produce the corresponding periods, switch boundary, and edge smoothing.

The required trace names are: `time`, `VDD`, `VSS`, `CLK`.

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
