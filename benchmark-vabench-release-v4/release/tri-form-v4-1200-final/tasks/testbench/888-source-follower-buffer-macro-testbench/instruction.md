# Source-follower Buffer Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Source-follower Buffer Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_OR_LOW_ENABLE_DRIVES_THE`: Reset or low `enable` drives the output and metrics low.
- `P_WHEN_ENABLED_THE_OUTPUT_FOLLOWS_VIN`: When enabled, the output follows `vin - vgs_drop`.
- `P_CLAMP_THE_OUTPUT_BETWEEN_VSS_AND`: Clamp the output between `vss` and `vbias - min_headroom`.
- `P_HEADROOM_METRIC_REPORTS_THE_REMAINING_VBIAS`: `headroom_metric` reports the remaining `vbias - vout` margin clipped to the nominal flag range.
- `P_VALID_IS_HIGH_ONLY_WHEN_ENABLED`: `valid` is high only when enabled, not reset, and the bias rail can support at least the minimum headroom.

The required trace names are: `time`, `vin`, `vbias`, `enable`, `rst`, `vout`, `headroom_metric`, `valid`.

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
