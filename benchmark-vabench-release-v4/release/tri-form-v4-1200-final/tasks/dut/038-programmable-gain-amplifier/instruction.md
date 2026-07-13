# Programmable Gain Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `programmable_gain_amplifier.va`: `programmable_gain_amplifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_UNITY`: While rst is active, the sampled gain is unity, out is vcm, and metric is low.
- `P_SAMPLED_GAIN_SELECT`: Each rising clk crossing with reset inactive samples gain_sel, selecting gain_high above vth and gain_low below vth; the selection holds between crossings.
- `P_COMMON_MODE_GAIN`: The unclamped output target is vcm plus the sampled gain times vin minus vcm.
- `P_OUTPUT_CLAMP`: Out is limited to the inclusive vmin through vmax range with finite smoothing.
- `P_CLIP_METRIC`: Metric is high exactly when the unclamped target lies outside vmin through vmax, and low otherwise; reset forces it low.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `programmable_gain_amplifier.va`.
Do not add or omit artifacts.
