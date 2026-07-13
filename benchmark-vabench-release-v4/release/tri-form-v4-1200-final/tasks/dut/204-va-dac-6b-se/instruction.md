# VA DAC 6b SE

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `va_dac_6b_se.va`: `va_dac_6b_se`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_EACH_RISING_RDY_CROSSING_SAMPLE`: On each rising `rdy` crossing, sample `din0..din5` with switched weights `0.5, 1, 2, 4, 8, 16` from `din0` through `din5`. Map the sampled weighted code to a bipolar single-ended output scaled by `vdd` using this public normalization:
- `P_TEXT_WEIGHTED_CODE_16_DIN5_8`: ```text weighted_code = 16*din5 + 8*din4 + 4*din3 + 2*din2 + 1*din1 + 0.5*din0 aout = (weighted_code / 47.5) * 2.0 * vdd - vdd ```
- `P_EACH_DIN_TERM_IS_1_WHEN`: Each `din*` term is `1` when the corresponding voltage is above `vth` and `0` otherwise. The denominator `47.5` is the fixed source normalization basis including the non-switching reference contribution.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `va_dac_6b_se.va`.
Do not add or omit artifacts.
