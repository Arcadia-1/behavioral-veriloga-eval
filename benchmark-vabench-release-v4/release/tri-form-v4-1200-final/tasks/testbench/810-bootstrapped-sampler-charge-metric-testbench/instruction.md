# Bootstrapped Sampler Charge Metric Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bootstrapped Sampler Charge Metric` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear held output, bootstrap metric, and droop flag.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, capture `vin` into `vhold`.
- `P_EXPOSE_A_BOOT_METRIC_THAT_INCREASES`: Expose a `boot_metric` that increases when the sampled input is near the rails and decreases near common-mode.
- `P_BETWEEN_SAMPLES_HOLD_VHOLD_AND_APPLY`: Between samples, hold `vhold` and apply a bounded droop step toward `vcm`.
- `P_ASSERT_DROOP_FLAG_WHEN_ACCUMULATED_HOLD`: Assert `droop_flag` when accumulated hold error exceeds `droop_tol`.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `vhold`, `boot_metric`, `droop_flag`.

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
