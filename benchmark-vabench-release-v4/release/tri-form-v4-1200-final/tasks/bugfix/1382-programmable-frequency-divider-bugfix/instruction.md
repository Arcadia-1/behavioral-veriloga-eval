# Programmable Frequency Divider Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `programmable_frequency_divider.va`: `programmable_frequency_divider`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_LOW_ENABLE_CLEARS_THE`: Reset or low `enable` clears the divider state, `clk_div`, `ratio_metric`, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_IN`: On each enabled rising `clk_in` edge, sample the four control bits and form divisor `N = code + 1`.
- `P_TOGGLE_CLK_DIV_WHENEVER_N_ENABLED`: Toggle `clk_div` whenever `N` enabled input-clock rising edges have been counted.
- `P_RATIO_METRIC_EXPOSES_THE_SAMPLED_DIVISOR`: `ratio_metric` exposes the sampled divisor as a voltage-coded fraction of the 1-to-16 range.
- `P_VALID_IS_HIGH_AFTER_THE_FIRST`: `valid` is high after the first divider toggle and low before that or during reset/disable.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `programmable_frequency_divider.va`.
Every supplied `.va` file is editable; do not add or omit files.
