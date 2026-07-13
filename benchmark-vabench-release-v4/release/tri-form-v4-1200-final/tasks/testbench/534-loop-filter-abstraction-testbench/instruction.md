# Loop Filter Abstraction Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Loop Filter Abstraction` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_STATE`: Active reset restores the proportional state to 0.45 V, the step to 0.20 V, the integral residual and accepted-update count to zero, and metric to 0 V.
- `P_DEADBAND_HOLD`: At a rising clk crossing, an error vin - 0.45 V whose magnitude does not exceed deadband produces no proportional, integral, step, or count update.
- `P_SIGNED_UPDATE`: Each accepted positive error increases the proportional state by the current step and each accepted negative error decreases it, while the integral residual accumulates 0.04 times the sampled error.
- `P_STEP_HALVING`: The proportional step halves after every accepted update, producing successively smaller proportional corrections for equal-sign errors.
- `P_LOCK_COUNT_METRIC`: Metric remains low for fewer than four accepted updates and is 0.9 V once the accepted-update count reaches four; reset clears it.
- `P_PROPORTIONAL_CLAMP`: The proportional state is clamped to 0.05 V through 0.85 V before the accumulated integral residual is added to form out.

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
