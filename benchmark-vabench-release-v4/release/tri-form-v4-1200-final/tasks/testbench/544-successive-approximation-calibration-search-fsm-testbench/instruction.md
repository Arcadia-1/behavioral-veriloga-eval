# Successive Approximation Calibration Search FSM Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Successive Approximation Calibration Search FSM` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_SEARCH_STATE`: Active reset restores out to target, the current step to step_init, the cycle count to zero, and metric low.
- `P_SIGNED_TRIAL_UPDATE`: On each active rising clk update before completion, vin above target increases out by the current step and vin below target decreases it.
- `P_SUCCESSIVE_STEP_HALVING`: The current step halves after every active decision update, yielding the public successive-approximation sequence from step_init.
- `P_FOUR_STEP_DONE`: Metric asserts after four active search updates and subsequent rising clocks hold the completed trial state until reset.
- `P_TRIM_CLAMP`: Out remains within vmin through vmax for every trial update.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`.

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
