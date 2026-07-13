# Bootstrapped Sampler Charge Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bootstrapped_sampler_charge_metric.va`: `bootstrapped_sampler_charge_metric`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear held output, bootstrap metric, and droop flag.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, capture `vin` into `vhold`.
- `P_EXPOSE_A_BOOT_METRIC_THAT_INCREASES`: Expose a `boot_metric` that increases when the sampled input is near the rails and decreases near common-mode.
- `P_BETWEEN_SAMPLES_HOLD_VHOLD_AND_APPLY`: Between samples, hold `vhold` and apply a bounded droop step toward `vcm`.
- `P_ASSERT_DROOP_FLAG_WHEN_ACCUMULATED_HOLD`: Assert `droop_flag` when accumulated hold error exceeds `droop_tol`.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bootstrapped_sampler_charge_metric.va`.
Do not add or omit artifacts.
