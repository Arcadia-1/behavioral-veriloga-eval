# Baseband Offset-and-gain Trim Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `baseband_offset_gain_trim_macro.va`: `baseband_offset_gain_trim_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to common mode, clears residual metric, and clears `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_SAMPLE`: On each enabled rising `clk`, sample gain and offset trim codes.
- `P_USE_GAIN_GAIN_BASE_GAIN_STEP`: Use `gain = gain_base + gain_step * gain_code`.
- `P_USE_SIGNED_OFFSET_OFFSET_CODE_3`: Use signed offset `(offset_code - 3) * offset_lsb`.
- `P_DRIVE_VOUT_AS_THE_CLIPPED_GAIN`: Drive `vout` as the clipped gain-and-offset adjusted input around common mode.
- `P_RESIDUAL_METRIC_REPORTS_THE_ABSOLUTE_OUTPUT`: `residual_metric` reports the absolute output distance from common mode and `valid` marks that a trim sample has occurred.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `baseband_offset_gain_trim_macro.va`.
Do not add or omit artifacts.
