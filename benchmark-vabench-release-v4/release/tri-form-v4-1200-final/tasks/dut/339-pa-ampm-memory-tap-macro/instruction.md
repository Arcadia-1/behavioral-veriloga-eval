# PA AM/PM Memory Tap Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pa_ampm_memory_tap_macro.va`: `pa_ampm_memory_tap_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metrics, and clear `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample input amplitude and drive level.
- `P_APPLY_AN_AM_GAIN_COMPRESSION_PROXY`: Apply an AM gain compression proxy as drive increases.
- `P_APPLY_A_ONE_SAMPLE_MEMORY_TERM`: Apply a one-sample memory term that changes output polarity metric after large input changes.
- `P_EXPOSE_AM_AND_PM_PROXIES_SEPARATELY`: Expose AM and PM proxies separately and assert `valid` after the first update.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pa_ampm_memory_tap_macro.va`.
Do not add or omit artifacts.
