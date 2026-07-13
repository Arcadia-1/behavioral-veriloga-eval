# Unary DAC Glitch-energy Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `unary_dac_glitch_energy_metric.va`: `unary_dac_glitch_energy_metric`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, previous code, glitch metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode the 3-bit code as a unary element count.
- `P_DRIVE_VOUT_PROPORTIONAL_TO_THE_DECODED`: Drive `vout` proportional to the decoded count.
- `P_DRIVE_GLITCH_METRIC_PROPORTIONAL_TO_THE`: Drive `glitch_metric` proportional to the absolute change in count since the previous enabled update.
- `P_ASSERT_VALID_AFTER_THE_FIRST_ENABLED`: Assert `valid` after the first enabled code update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `unary_dac_glitch_energy_metric.va`.
Do not add or omit artifacts.
