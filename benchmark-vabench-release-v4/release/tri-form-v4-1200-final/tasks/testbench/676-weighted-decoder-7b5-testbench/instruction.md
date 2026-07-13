# Weighted Decoder 7b5 Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Weighted Decoder 7b5` DUT. The evaluator runs the same submitted bytes
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

- `P_SHARED_272_DENOMINATOR`: All decoded outputs use the shared normalization denominator of 272.0, including the fixed reference basis.
- `P_SEVEN_BIT_OUTPUT`: `aout7b` reports the 7-bit decoded analog output with the specified redundant SAR weights.
- `P_SEVEN_HALF_BIT_OUTPUT`: `aout7b5` preserves the half-bit redundant contribution and correct polarity.
- `P_EIGHT_BIT_OUTPUT`: `aout8b` reports the full 8-bit weighted output with the correct amplitude.

The required trace names are: `time`, `d0`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `aout7b`, `aout7b5`, `aout8b`.

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
