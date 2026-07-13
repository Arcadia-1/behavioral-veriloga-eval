# Differential-pair gm Limiter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Differential-pair gm Limiter` DUT. The evaluator runs the same submitted bytes
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

- `P_WHEN_DISABLED_DRIVE_BOTH_OUTPUTS_TO`: When disabled, drive both outputs to `vcm`, clear `gm_metric`, and clear `limit_flag`.
- `P_WHEN_ENABLED_CONVERT_THE_SAMPLED_DIFFERENTIAL`: When enabled, convert the sampled differential input into equal-and-opposite output deviations around `vcm`.
- `P_SCALE_SMALL_SIGNAL_OUTPUT_SEPARATION_BY`: Scale small-signal output separation by `gm_gain` and compress large differential inputs smoothly at `diff_limit`.
- `P_DRIVE_GM_METRIC_AS_A_VOLTAGE`: Drive `gm_metric` as a voltage-coded estimate of the active transconductance region.
- `P_ASSERT_LIMIT_FLAG_ONLY_WHEN_COMPRESSION`: Assert `limit_flag` only when compression is active.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vinp`, `vinn`, `bias`, `enable`, `voutp`, `voutn`, `gm_metric`, `limit_flag`.

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
