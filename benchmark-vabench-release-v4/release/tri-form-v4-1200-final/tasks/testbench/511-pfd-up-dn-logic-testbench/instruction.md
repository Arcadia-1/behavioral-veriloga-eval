# PFD Up DN Logic Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PFD Up DN Logic` DUT. The evaluator runs the same submitted bytes
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

- `P_REF_SETS_UP`: A rising REF edge asserts UP, and falling REF edges do not set either output.
- `P_DIV_SETS_DN`: A rising DIV edge asserts DN, and falling DIV edges do not set either output.
- `P_RESET_RACE_CLEAR`: If a rising edge arrives while the opposite output state is already high, both UP and DN clear immediately for REF-leading and DIV-leading orderings.
- `P_NO_PERSISTENT_OVERLAP`: UP and DN are not intentionally held high together beyond finite transition smoothing overlap.
- `P_RAIL_REFERENCE`: UP and DN high levels track the local VDD rail and low levels track the local VSS rail.

The required trace names are: `time`, `vdd`, `vss`, `ref`, `div`, `up`, `dn`.

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
