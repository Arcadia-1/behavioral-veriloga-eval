# Differential Buffer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Differential Buffer` DUT. The evaluator runs the same submitted bytes
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

- `P_POSITIVE_UNITY`: VOUTP continuously follows VINP with unity voltage gain and unchanged polarity.
- `P_NEGATIVE_UNITY`: VOUTN continuously follows VINN with unity voltage gain and unchanged polarity.
- `P_CHANNEL_INDEPENDENCE`: Each output depends on its corresponding input and is not cross-coupled to the opposite input.
- `P_DIFFERENTIAL_PRESERVATION`: The differential output VOUTP minus VOUTN equals the differential input VINP minus VINN.
- `P_COMMON_MODE_PRESERVATION`: The output pair preserves the input pair common-mode voltage without conversion or rail logic.

The required trace names are: `time`, `vinp`, `vinn`, `voutp`, `voutn`.

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
