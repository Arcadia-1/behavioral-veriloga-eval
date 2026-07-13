# Sync 8b DFFs V2 Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sync 8b DFFs V2` DUT. The evaluator runs the same submitted bytes
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

- `P_PHASED_CAPTURE_ORDER`: Each phase clock captures its corresponding `dl` input and shifts previously captured upper-phase data down the chain in the specified order.
- `P_INTERMEDIATE_OUTPUT_CAPTURE`: Intermediate outputs, including `do4`, reflect their synchronized pipeline state rather than a stuck or skipped stage.
- `P_FINAL_OUTPUT_CAPTURE`: The most delayed output `do8` reflects the final synchronized stage with correct polarity.
- `P_FULL_LEVEL_OUTPUTS`: All `do` outputs drive full voltage-coded levels for their captured state.

The required trace names are: `time`, `ck1`, `ck2`, `ck3`, `ck4`, `ck5`, `ck6`, `ck7`, `ck8`, `ck9`, `dl0`, `dl1`, `dl2`, `dl3`, `dl4`, `dl5`, `dl6`, `dl7`, `dl8`, `do0`, `do1`, `do2`, `do3`, `do4`, `do5`, `do6`, `do7`, `do8`.

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
