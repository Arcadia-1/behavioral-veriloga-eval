# SAR DAS Logic 6b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SAR DAS Logic 6b` DUT. The evaluator runs the same submitted bytes
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

- `P_SAMPLING_RESET_CONVERSION_STATE`: A rising `clk_sampling` transition clears controls and pulses, and a falling transition arms the SAR conversion sequence.
- `P_SAR_COMPARATOR_POLARITY`: Each rising `clk_sar` transition compares `vcomp` to `vcm` and drives `co/cob` with the declared polarity.
- `P_SIX_BIT_DECISION_SEQUENCE`: The SAR decisions update `d6..d1` in the declared order through the conversion.
- `P_CONTROL_OUTPUT_LEVELS`: Decision pulses and bit-control outputs use valid voltage-coded low/high levels.

The required trace names are: `time`, `clk_sampling`, `clk_sar`, `co`, `cob`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `db1`, `db2`, `db3`, `db4`, `db5`, `db6`, `vcomp`.

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
