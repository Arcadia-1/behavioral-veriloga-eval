# CTLE Equalizer Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ctle_equalizer.va`: `ctle_equalizer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_INITIALIZES_THE_EQUALIZED_OUTPUT_TO`: Reset initializes the equalized output to common mode and clears metric outputs.
- `P_ON_EACH_RISING_CLK_SAMPLE_THE`: On each rising `clk`, sample the boost code and the current input.
- `P_DRIVE_VOUT_FROM_THE_CURRENT_INPUT`: Drive `vout` from the current input plus a boost-code-scaled edge term relative to the previous sampled input.
- `P_CLAMP_VOUT_TO_THE_VSS_TO`: Clamp `vout` to the `vss` to `vdd` range.
- `P_EDGE_METRIC_REPORTS_THE_ABSOLUTE_BOOSTED`: `edge_metric` reports the absolute boosted edge contribution after clipping to full scale.
- `P_SAT_FLAG_IS_HIGH_WHEN_THE`: `sat_flag` is high when the unclamped equalized target would exceed either output rail.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ctle_equalizer.va`.
Do not add or omit artifacts.
