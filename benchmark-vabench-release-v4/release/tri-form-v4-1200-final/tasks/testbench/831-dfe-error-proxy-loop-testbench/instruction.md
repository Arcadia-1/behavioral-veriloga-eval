# DFE Error-proxy Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DFE Error-proxy Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear taps, corrected output, error metric, and `converged`.
- `P_ON_EACH_ENABLED_DECISION_CLOCK_LATCH`: On each enabled decision clock, latch the sign of `sample_in - vcm` as the current decision.
- `P_USE_THE_PREVIOUS_DECISION_HISTORY_TO`: Use the previous decision history to subtract a two-tap feedback estimate from the live sample.
- `P_EXPOSE_THE_ABSOLUTE_RESIDUAL_ON_ERROR`: Expose the absolute residual on `error_metric`.
- `P_ASSERT_CONVERGED_WHEN_THE_RESIDUAL_REMAINS`: Assert `converged` when the residual remains below `residual_tol` for three decisions.

The required trace names are: `time`, `sample_in`, `decision_clk`, `rst`, `enable`, `tap_1`, `tap_0`, `corrected_out`, `error_metric`, `converged`.

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
