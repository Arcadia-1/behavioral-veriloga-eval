# Segmented DAC with DEM Control Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Segmented DAC with DEM Control` DUT. The evaluator runs the same submitted bytes
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

- `P_DEM_RESET_CLEAR`: Reset clears vout, unit selection mask, and rotation pointer.
- `P_DEM_DAC_TRANSFER`: Each rising clock samples the unsigned 6-bit code and drives vref times code divided by 63.
- `P_DEM_ROTATED_MASK`: The selection mask contains the requested number of consecutive circular unit elements starting at the prior pointer.
- `P_DEM_POINTER_ADVANCE`: After each update the pointer advances by the requested unit count modulo eight.

The required trace names are: `time`, `clk`, `rst`, `code_5`, `code_4`, `code_3`, `code_2`, `code_1`, `code_0`, `vout`, `sel_7`, `sel_6`, `sel_5`, `sel_4`, `sel_3`, `sel_2`, `sel_1`, `sel_0`, `ptr_2`, `ptr_1`, `ptr_0`.

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
