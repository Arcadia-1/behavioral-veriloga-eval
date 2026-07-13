# Bootstrapped Sampler Charge Metric Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bootstrapped_sampler_charge_metric.va`: `bootstrapped_sampler_charge_metric`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear held output, bootstrap metric, and droop flag.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, capture `vin` into `vhold`.
- `P_EXPOSE_A_BOOT_METRIC_THAT_INCREASES`: Expose a `boot_metric` that increases when the sampled input is near the rails and decreases near common-mode.
- `P_BETWEEN_SAMPLES_HOLD_VHOLD_AND_APPLY`: Between samples, hold `vhold` and apply a bounded droop step toward `vcm`.
- `P_ASSERT_DROOP_FLAG_WHEN_ACCUMULATED_HOLD`: Assert `droop_flag` when accumulated hold error exceeds `droop_tol`.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bootstrapped_sampler_charge_metric.va`.
Every supplied `.va` file is editable; do not add or omit files.
