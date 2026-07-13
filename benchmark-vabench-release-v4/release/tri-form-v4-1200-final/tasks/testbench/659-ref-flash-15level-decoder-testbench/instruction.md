# Ref Flash 15level Decoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Ref Flash 15level Decoder` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_FIFTEEN_TAP_COUNT`: Each rising `clks` crossing counts voltage-coded assertions across the 15 tap inputs.
- `P_FULL_TAP_COVERAGE`: Upper and lower tap inputs all contribute to the count; no subset of taps is ignored.
- `P_FRACTION_NORMALIZATION_AND_GAIN`: `dout` reports the count divided by 15 without additional gain scaling.

The required trace names are: `time`, `clks`, `dout`, `dt0`, `dt1`, `dt10`, `dt11`, `dt12`, `dt13`, `dt14`, `dt2`, `dt3`, `dt4`, `dt5`, `dt6`, `dt7`, `dt8`, `dt9`.

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
