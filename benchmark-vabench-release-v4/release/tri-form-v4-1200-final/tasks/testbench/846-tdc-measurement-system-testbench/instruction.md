# TDC Event Measurement System Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `TDC Event Measurement System` DUT. The evaluator runs the same submitted bytes
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

- `P_TDC_RESET_CLEAR`: Reset clears count code, valid, and overflow.
- `P_TDC_RESTART_CLEAR`: Each rising start edge begins a new interval and clears valid and overflow.
- `P_TDC_INTERVAL_COUNT`: The first stop after start latches the number of intervening rising clock edges.
- `P_TDC_VALID_LATCH`: A completed interval asserts valid and preserves its code until restart or reset.
- `P_TDC_OVERFLOW`: The 256th armed clock saturates code at 255, asserts overflow and valid, and disarms.

The required trace names are: `time`, `start`, `stop`, `clk`, `rst`, `code_7`, `code_6`, `code_5`, `code_4`, `code_3`, `code_2`, `code_1`, `code_0`, `valid`, `overflow`.

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
