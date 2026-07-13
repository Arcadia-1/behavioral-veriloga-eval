# Programmable Frequency Divider

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `programmable_frequency_divider.va`: `programmable_frequency_divider`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_OR_LOW_ENABLE_CLEARS_THE`: Reset or low `enable` clears the divider state, `clk_div`, `ratio_metric`, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_IN`: On each enabled rising `clk_in` edge, sample the four control bits and form divisor `N = code + 1`.
- `P_TOGGLE_CLK_DIV_WHENEVER_N_ENABLED`: Toggle `clk_div` whenever `N` enabled input-clock rising edges have been counted.
- `P_RATIO_METRIC_EXPOSES_THE_SAMPLED_DIVISOR`: `ratio_metric` exposes the sampled divisor as a voltage-coded fraction of the 1-to-16 range.
- `P_VALID_IS_HIGH_AFTER_THE_FIRST`: `valid` is high after the first divider toggle and low before that or during reset/disable.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `programmable_frequency_divider.va`.
Do not add or omit artifacts.
