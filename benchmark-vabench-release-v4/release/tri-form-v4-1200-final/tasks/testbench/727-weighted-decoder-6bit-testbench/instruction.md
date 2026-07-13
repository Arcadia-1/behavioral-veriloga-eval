# Weighted Decoder 6bit Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Weighted Decoder 6bit` DUT. The evaluator runs the same submitted bytes
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

- `P_TREAT_EACH_INPUT_AS_LOGIC_1`: Treat each input as logic 1 when its voltage is greater than `vth`, otherwise logic 0.
- `P_INTERPRET_VD1_VD6_AS_AN_UNSIGNED`: Interpret `vd1..vd6` as an unsigned binary word with `vd1` as MSB and `vd6` as LSB.
- `P_SCALE_THE_DECODED_CODE_BY_VREF`: Scale the decoded code by `vref`.
- `P_MAP_ALL_ZERO_INPUT_TO_0`: Map all-zero input to 0 V.
- `P_MAP_ALL_ONES_INPUT_TO_VREF`: Map all-ones input to `vref`.

The required trace names are: `time`, `vd1`, `vd2`, `vd3`, `vd4`, `vd5`, `vd6`, `vout`.

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
