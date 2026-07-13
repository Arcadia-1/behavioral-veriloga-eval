# Resistor Ladder Monotonic Decoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Resistor Ladder Monotonic Decoder` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` low, clear `step_metric`, and clear `monotonic_ok`.
- `P_DECODE_CODE_2_CODE_0_AS`: Decode `code_2..code_0` as an unsigned ladder tap index from 0 to 7.
- `P_DRIVE_VOUT_TO_THE_CORRESPONDING_EVENLY`: Drive `vout` to the corresponding evenly spaced ladder voltage between `vss` and `vdd`.
- `P_EXPOSE_ONE_LSB_STEP_ON_STEP`: Expose one LSB step on `step_metric` while enabled.
- `P_ASSERT_MONOTONIC_OK_WHEN_THE_ACTIVE`: Assert `monotonic_ok` when the active code-to-output mapping is nondecreasing.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `code_2`, `code_1`, `code_0`, `enable`, `rst`, `vout`, `step_metric`, `monotonic_ok`.

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
