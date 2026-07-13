# Baseband Anti-alias Filter Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `baseband_antialias_filter_macro.va`: `baseband_antialias_filter_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metric, and clear `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode `bw_1..bw_0` as a bandwidth setting.
- `P_UPDATE_VOUT_AS_A_FIRST_ORDER`: Update `vout` as a first-order discrete-time low-pass response to `vin`.
- `P_HIGHER_BANDWIDTH_CODE_MUST_MOVE_VOUT`: Higher bandwidth code must move `vout` closer to `vin` per update.
- `P_EXPOSE_THE_ACTIVE_BANDWIDTH_CODE_ON`: Expose the active bandwidth code on `bandwidth_metric` and assert `valid` after the first update.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `baseband_antialias_filter_macro.va`.
Do not add or omit artifacts.
