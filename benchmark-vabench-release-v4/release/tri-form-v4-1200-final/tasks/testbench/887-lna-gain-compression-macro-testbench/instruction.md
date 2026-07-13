# LNA Gain-compression Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LNA Gain-compression Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `gain_metric`, and clear `compression_flag`.
- `P_WHEN_ENABLED_PROVIDE_HIGH_GAIN_FOR`: When enabled, provide high gain for small input deviations around `vcm`.
- `P_REDUCE_EFFECTIVE_GAIN_MONOTONICALLY_WHEN_THE`: Reduce effective gain monotonically when the absolute input deviation exceeds `input_clip`.
- `P_EXPOSE_ACTIVE_GAIN_ON_GAIN_METRIC`: Expose active gain on `gain_metric` and assert `compression_flag` during compressed operation.
- `P_CLAMP_VOUT_INSIDE_VSS_VDD`: Clamp `vout` inside `[vss, vdd]`.

The required trace names are: `time`, `vin`, `enable`, `rst`, `vout`, `gain_metric`, `compression_flag`.

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
