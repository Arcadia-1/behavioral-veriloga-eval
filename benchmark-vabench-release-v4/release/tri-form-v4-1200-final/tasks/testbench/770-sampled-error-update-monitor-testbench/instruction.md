# Sampled Error Update Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sampled Error Update Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEARS_STATE_AND_OBSERVABLES`: While rst is high at a rising clock edge, clear the stable count, out, err_metric, and progress.
- `P_CORRECTED_OUTPUT_USES_SAMPLE_TARGET_AND_COEF`: At each enabled rising clock edge, compute the clipped coefficient and drive the clamped corrected sample from sample, target, and coef.
- `P_ERROR_METRIC_REPORTS_ABSOLUTE_ERROR`: Drive err_metric from the bounded absolute target-minus-sample error.
- `P_PROGRESS_COUNTS_CONSECUTIVE_IN_WINDOW_SAMPLES`: Increment progress only for consecutive in-window sampled errors, clear it on an out-of-window sample, and saturate at ready_count.

The required trace names are: `time`, `clk`, `rst`, `sample`, `target`, `coef`, `out`, `err_metric`, `progress`.

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
