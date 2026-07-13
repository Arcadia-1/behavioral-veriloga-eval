# CDR Eye Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `CDR Eye Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear early/late flags, eye metric, lock hint, and `valid`.
- `P_ON_EACH_SAMPLING_CLOCK_EDGE_COMPARE`: On each sampling-clock edge, compare the sampled data level with the previous sample.
- `P_RAISE_EARLY_OR_LATE_ACCORDING_TO`: Raise `early` or `late` according to the sign of the edge-position proxy around the sample instant.
- `P_DRIVE_EYE_METRIC_FROM_RECENT_TRANSITION`: Drive `eye_metric` from recent transition stability and sample margin.
- `P_ASSERT_LOCK_HINT_AFTER_FOUR_CONSECUTIVE`: Assert `lock_hint` after four consecutive samples with eye metric above `eye_min`.

The required trace names are: `time`, `data_in`, `sample_clk`, `rst`, `enable`, `early`, `late`, `eye_metric`, `lock_hint`, `valid`.

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
