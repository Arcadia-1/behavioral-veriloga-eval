# Fixed-frequency Oscillator Source Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Fixed-frequency Oscillator Source` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `osc_out`, `period_metric`, and `valid` low.
- `P_WHEN_ENABLED_GENERATE_A_PERIODIC_VOLTAGE`: When enabled, generate a periodic voltage-domain clock that toggles between `vss` and `vdd` with the configured period.
- `P_PERIOD_METRIC_MUST_EXPOSE_A_STABLE`: `period_metric` must expose a stable voltage-coded representation of the configured period after the first complete cycle.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETE`: Assert `valid` after the first complete oscillator cycle following enable.
- `P_RESET_OR_DISABLE_MUST_RESTART_THE`: Reset or disable must restart the oscillator phase deterministically.

The required trace names are: `time`, `enable`, `rst`, `osc_out`, `period_metric`, `valid`.

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
