# Periodic Sampler with Aperture Metric Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `periodic_sampler_aperture_metric.va`: `periodic_sampler_aperture_metric`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEARS_THE_HELD_VALUE_APERTURE`: Reset clears the held value, aperture metric, and valid flag.
- `P_ON_EACH_RISING_CLK_EDGE_WITH`: On each rising `clk` edge with `sample_en` high, capture `vin` into `vhold`.
- `P_THE_APERTURE_METRIC_AFTER_A_CAPTURE`: The aperture metric after a capture is proportional to the absolute difference between the new sample and the previous held sample.
- `P_HOLD_VHOLD_AND_THE_LAST_METRIC`: Hold `vhold` and the last metric between enabled sampling events.
- `P_VALID_IS_HIGH_AFTER_THE_FIRST`: `valid` is high after the first enabled sample and low during reset.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `periodic_sampler_aperture_metric.va`.
Every supplied `.va` file is editable; do not add or omit files.
