# Settling Window Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Settling Window Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_WINDOW_DEFINITION`: The input is qualified in-window exactly while the absolute vin-to-target error is no greater than tol.
- `P_ENTRY_AND_HOLD`: Entering the window records the entry time, but settled remains low until vin has stayed continuously in-window for at least 20 ns.
- `P_EXIT_RESETS_QUALIFICATION`: Leaving the tolerance window before or after qualification clears the entry state, drives settled low, and clears the time code.
- `P_ENTRY_TIME_CODE`: After qualification, t_code[7:0] reports the rounded window-entry time in whole nanoseconds, saturated to 0 through 255.
- `P_BIT_ORDER_AND_LEVELS`: t_code0 is the least significant bit and t_code7 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

The required trace names are: `time`, `vin`, `target`, `tol`, `settled`, `t_code0`, `t_code1`, `t_code2`, `t_code3`, `t_code4`, `t_code5`, `t_code6`, `t_code7`.

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
