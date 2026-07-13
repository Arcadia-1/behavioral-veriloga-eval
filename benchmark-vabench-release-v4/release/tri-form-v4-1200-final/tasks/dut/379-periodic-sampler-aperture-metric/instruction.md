# Periodic Sampler with Aperture Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `periodic_sampler_aperture_metric.va`: `periodic_sampler_aperture_metric`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEARS_THE_HELD_VALUE_APERTURE`: Reset clears the held value, aperture metric, and valid flag.
- `P_ON_EACH_RISING_CLK_EDGE_WITH`: On each rising `clk` edge with `sample_en` high, capture `vin` into `vhold`.
- `P_THE_APERTURE_METRIC_AFTER_A_CAPTURE`: The aperture metric after a capture is proportional to the absolute difference between the new sample and the previous held sample.
- `P_HOLD_VHOLD_AND_THE_LAST_METRIC`: Hold `vhold` and the last metric between enabled sampling events.
- `P_VALID_IS_HIGH_AFTER_THE_FIRST`: `valid` is high after the first enabled sample and low during reset.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `periodic_sampler_aperture_metric.va`.
Do not add or omit artifacts.
