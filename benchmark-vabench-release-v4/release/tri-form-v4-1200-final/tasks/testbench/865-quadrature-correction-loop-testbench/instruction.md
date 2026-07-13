# Quadrature Correction Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Quadrature Correction Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEAR`: Reset clears both trim buses, corrected outputs, error metric, and lock state.
- `P_TRIM_DIRECTION`: Enabled calibration updates signed gain and phase trim codes in directions that reduce measured amplitude and quadrature errors.
- `P_CORRECTION_APPLICATION`: Corrected I and Q outputs apply the currently exposed gain and phase trim codes and remain bounded by the supplies.
- `P_LOCK_HOLD`: Lock asserts after three consecutive in-tolerance calibration updates, and disabling calibration holds codes while correction remains active.

The required trace names are: `time`, `i_in`, `q_in`, `clk`, `rst`, `cal_en`, `i_out`, `q_out`, `gain_code_3`, `gain_code_2`, `gain_code_1`, `gain_code_0`, `phase_code_3`, `phase_code_2`, `phase_code_1`, `phase_code_0`, `error_metric`, `locked`.

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
