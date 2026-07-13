# Trim Ctrl 4bit Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Trim Ctrl 4bit` DUT. The evaluator runs the same submitted bytes
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

- `P_ANALOG_INPUT_ROUNDING`: Round `ain` to the nearest integer code level rather than truncating.
- `P_LOW_FOUR_BIT_MAPPING`: Emit the low four bits of the rounded code on `dout0..dout3` in the declared bit order.
- `P_CONTINUOUS_CODE_UPDATE`: Update deterministically as `ain` changes without requiring hidden state or clocks.
- `P_TRIM_OUTPUT_LEVELS`: All trim outputs are voltage-coded at valid low/high levels.

The required trace names are: `time`, `ain`, `dout0`, `dout1`, `dout2`, `dout3`.

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
