# LT Read SAR7B Weighted Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LT Read SAR7B Weighted` DUT. The evaluator runs the same submitted bytes
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

- `P_CONTINUOUSLY_DRIVE`: Continuously drive:
- `P_TEXT_VOUT_VREF_VREF_D7_D6`: ```text vout = -vref + vref * (d7 + d6/2 + d5/4 + d4/8 + d3/16 + d2/32 + d1/64 + d0/128) ```
- `P_WHERE_EACH_D_TERM_IS_1`: where each `d` term is `1` when the corresponding input voltage is above `vth` and `0` otherwise.

The required trace names are: `time`, `d0`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `vout`, `gnd`.

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
