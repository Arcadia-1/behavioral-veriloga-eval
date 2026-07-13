# Clock Divider Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clock Divider` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET`: Active-low reset clears divider phase and drives clk_out and lock low.
- `P_RATIO_DECODE`: The LSB-first 8-bit code selects the divide ratio, with code zero mapped to ratio one.
- `P_DIVIDED_PERIOD`: For ratios above one, successive clk_out rising edges span the decoded number of clk_in rising edges.
- `P_ODD_RATIO_DUTY`: Odd ratios retain both phases with floor/ceil segment lengths differing by at most one input cycle.
- `P_LOCK_REACQUIRE`: lock asserts after one complete output period and clears/reacquires when the ratio changes.

The required trace names are: `time`, `clk_in`, `rst_n`, `clk_out`, `lock`, `div_code_0`, `div_code_1`, `div_code_2`, `div_code_3`, `div_code_4`, `div_code_5`, `div_code_6`, `div_code_7`.

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
