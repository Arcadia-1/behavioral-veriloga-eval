# Offset-cancellation Servo Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Offset-cancellation Servo` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: On reset, clear trim code, corrected output, error metric, and done; when calibration is disabled, do not advance trim search state.
- `P_TRIM_SEARCH_DIRECTION`: Update the signed 5-bit trim code in the direction that reduces sampled differential error.
- `P_CORRECTED_RESIDUAL`: Drive corrected_out as the differential input minus the signed trim correction.
- `P_ERROR_METRIC`: Expose the current residual offset on error_metric after each enabled trim update.
- `P_DONE_QUALIFICATION`: Assert done only after four consecutive calibration updates with residual magnitude within error_tol.

The required trace names are: `time`, `vinp`, `vinn`, `clk`, `rst`, `cal_en`, `corrected_out`, `trim_4`, `trim_3`, `trim_2`, `trim_1`, `trim_0`, `error_metric`, `done`.

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
