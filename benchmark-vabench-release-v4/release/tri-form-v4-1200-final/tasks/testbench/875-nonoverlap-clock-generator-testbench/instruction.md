# Non-overlapping Clock Generator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Non-overlapping Clock Generator` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_OR_A_LOW_ENABLE_CLEARS`: Reset or a low `enable` clears both phases, `deadtime_metric`, and `valid`.
- `P_A_RISING_CLK_IN_REQUEST_EVENTUALLY`: A rising `clk_in` request eventually enables `phi1`; a falling `clk_in` request eventually enables `phi2`.
- `P_DURING_EACH_HANDOFF_BOTH_PHI1_AND`: During each handoff, both `phi1` and `phi2` remain low for the configured dead-time interval.
- `P_PHI1_AND_PHI2_MUST_NEVER_BE`: `phi1` and `phi2` must never be high at the same time.
- `P_DEADTIME_METRIC_IS_HIGH_ONLY_WHILE`: `deadtime_metric` is high only while a pending phase request is in the enforced both-low interval.
- `P_VALID_BECOMES_HIGH_AFTER_THE_FIRST`: `valid` becomes high after the first enabled handoff completes and remains high until reset or disable.

The required trace names are: `time`, `clk_in`, `rst`, `enable`, `phi1`, `phi2`, `deadtime_metric`, `valid`.

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
