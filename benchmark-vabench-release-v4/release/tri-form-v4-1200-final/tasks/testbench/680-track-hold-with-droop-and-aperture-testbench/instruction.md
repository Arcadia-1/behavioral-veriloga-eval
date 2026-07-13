# Track/Hold with Droop and Aperture Metric Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Track/Hold with Droop and Aperture Metric` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or a low `enable` clears `vhold`, `aperture_metric`, `droop_metric`, and `valid`.
- `P_TRACK_MODE_FOLLOWS_INPUT`: While `track` is high and the DUT is enabled, the held state follows `vin` at the internal update cadence and `valid` remains low.
- `P_FALLING_TRACK_SAMPLE_APERTURE`: A falling `track` edge samples `vin`, asserts `valid`, and reports an aperture metric proportional to the step from the previous tracked value.
- `P_HOLD_MODE_DROOP`: During hold mode, `vhold` droops downward by `droop_per_tick` on each update tick without going below `vss`.
- `P_DROOP_METRIC_ACCUMULATION`: `droop_metric` accumulates total hold-mode droop and clears on a new sample, reset, or disable.

The required trace names are: `time`, `vin`, `track`, `rst`, `enable`, `vhold`, `aperture_metric`, `droop_metric`, `valid`.

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
