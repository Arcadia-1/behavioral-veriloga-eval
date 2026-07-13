# Reference Ladder with Buffered Taps Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Reference Ladder with Buffered Taps` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive taps to `vss` and clear `monotonic_ok`.
- `P_WHEN_ENABLED_GENERATE_FOUR_EVENLY_SPACED`: When enabled, generate four evenly spaced buffered tap voltages between `vref_lo` and `vref_hi`.
- `P_CLAMP_REVERSED_OR_OUT_OF_RANGE`: Clamp reversed or out-of-range references into the public rail range before generating taps.
- `P_ASSERT_MONOTONIC_OK_ONLY_WHEN_THE`: Assert `monotonic_ok` only when the exposed tap sequence is nondecreasing.
- `P_SMOOTH_TAP_OUTPUT_TRANSITIONS_WITH_THE`: Smooth tap output transitions with the public transition parameter.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vref_hi`, `vref_lo`, `enable`, `rst`, `tap0`, `tap1`, `tap2`, `tap3`, `monotonic_ok`.

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
