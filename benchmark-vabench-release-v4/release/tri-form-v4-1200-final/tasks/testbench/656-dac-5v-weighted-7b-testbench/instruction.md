# DAC 5V Weighted 7b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DAC 5V Weighted 7b` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM`: Each rising `clks` crossing samples `din0` through `din6` into the declared seven-bit weighted DAC sum.
- `P_MSB_AND_TERMINATION_CONTRIBUTIONS`: `din0` contributes the largest switched weight and the fixed termination contribution is included.
- `P_REFERENCE_ENDPOINTS_AND_SCALE`: The output uses the declared `refp` and `refn` endpoints and full DAC scale.

The required trace names are: `time`, `clks`, `din0`, `din1`, `din2`, `din3`, `din4`, `din5`, `din6`, `vout`.

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
