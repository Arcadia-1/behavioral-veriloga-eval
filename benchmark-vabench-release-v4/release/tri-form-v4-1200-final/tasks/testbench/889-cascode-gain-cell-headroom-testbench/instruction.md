# Cascode Gain-cell Headroom Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Cascode Gain-cell Headroom Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to common mode and clears metrics.
- `P_WHEN_ENABLED_COMPUTE_AN_INVERTING_GAIN`: When enabled, compute an inverting gain-cell output around common mode.
- `P_CLAMP_THE_OUTPUT_BETWEEN_VSS_AND`: Clamp the output between `vss` and the available headroom limit.
- `P_GAIN_METRIC_REPORTS_THE_ABSOLUTE_OUTPUT`: `gain_metric` reports the absolute output excursion from common mode.
- `P_HEADROOM_OK_IS_HIGH_ONLY_WHEN`: `headroom_ok` is high only when the available headroom limit remains above common mode.

The required trace names are: `time`, `vin`, `vbias`, `vdd_sense`, `enable`, `rst`, `vout`, `gain_metric`, `headroom_ok`.

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
