# Auto-zero Comparator Preamplifier Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Auto-zero Comparator Preamplifier` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_CLEAR_STORED_OFFSET_DECISION`: On reset, clear stored offset, `decision`, and `ready`.
- `P_DURING_AN_AUTO_ZERO_CLOCK_UPDATE`: During an auto-zero clock update with `az_en` high, store the apparent differential offset between `vinp` and `vinn`.
- `P_DURING_AN_EVALUATION_CLOCK_UPDATE_WITH`: During an evaluation clock update with `eval_en` high, subtract the stored offset from the live differential input.
- `P_DRIVE_DECISION_HIGH_FOR_CORRECTED_NONNEGATIVE`: Drive `decision` high for corrected nonnegative differential input and low otherwise.
- `P_EXPOSE_STORED_OFFSET_ON_OFFSET_STORE`: Expose stored offset on `offset_store` and assert `ready` after at least one auto-zero update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vinp`, `vinn`, `clk`, `rst`, `az_en`, `eval_en`, `decision`, `offset_store`, `ready`.

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
