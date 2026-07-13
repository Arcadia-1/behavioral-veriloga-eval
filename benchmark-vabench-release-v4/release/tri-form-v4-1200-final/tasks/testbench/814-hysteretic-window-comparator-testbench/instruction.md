# Hysteretic Window Comparator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Hysteretic Window Comparator` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `inside_flag`, `state_metric`, and `toggled`.
- `P_USE_LOW_TRIP_AND_HIGH_TRIP`: Use `low_trip` and `high_trip` as public voltage thresholds.
- `P_ASSERT_INSIDE_FLAG_WHEN_VIN_ENTERS`: Assert `inside_flag` when `vin` enters the window and keep it asserted until `vin` crosses outside the hysteresis margins.
- `P_EXPOSE_THE_CURRENT_STATE_AS_STATE`: Expose the current state as `state_metric` and pulse `toggled` high on state changes.
- `P_DO_NOT_CHATTER_FOR_SMALL_INPUT`: Do not chatter for small input movement inside the hysteresis band.

The required trace names are: `time`, `vin`, `rst`, `enable`, `low_trip`, `high_trip`, `inside_flag`, `state_metric`, `toggled`.

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
