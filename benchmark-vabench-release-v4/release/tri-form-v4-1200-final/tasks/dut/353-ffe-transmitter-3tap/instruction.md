# 3-tap FFE Transmitter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ffe_tx_3tap.va`: `ffe_tx_3tap`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEARS_SYMBOL_HISTORY_AND_DRIVES`: Reset clears symbol history and drives all outputs to common mode.
- `P_ON_EACH_RISING_CLK_SAMPLE_DATA`: On each rising `clk`, sample `data` as +1 for high and -1 for low.
- `P_DRIVE_MAIN_DBG_PRE_DBG_AND`: Drive `main_dbg`, `pre_dbg`, and `post_dbg` as voltage-coded per-tap contributions around common mode.
- `P_VOUT_IS_THE_CLIPPED_SUM_OF`: `vout` is the clipped sum of the current main contribution, previous-symbol pre contribution, and older-symbol post contribution.
- `P_HIGHER_TAP_CONTROL_CODES_MUST_INCREASE`: Higher tap-control codes must increase the corresponding contribution magnitude.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ffe_tx_3tap.va`.
Do not add or omit artifacts.
