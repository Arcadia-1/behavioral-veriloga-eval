# Capacitive-feedback Amplifier Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Capacitive-feedback Amplifier Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `sampled_metric`, and clear `settled`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample `vin` and decode `gain_1..gain_0` as a programmable capacitor ratio.
- `P_DRIVE_SAMPLED_METRIC_WITH_THE_HELD`: Drive `sampled_metric` with the held input sample.
- `P_MOVE_VOUT_TOWARD_VCM_GAIN_SAMPLE`: Move `vout` toward `vcm + gain * (sample - vcm)` with bounded per-update movement.
- `P_ASSERT_SETTLED_AFTER_THE_OUTPUT_HAS`: Assert `settled` after the output has stayed within `settle_tol` of the target for two enabled updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `gain_1`, `gain_0`, `vout`, `sampled_metric`, `settled`.

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
