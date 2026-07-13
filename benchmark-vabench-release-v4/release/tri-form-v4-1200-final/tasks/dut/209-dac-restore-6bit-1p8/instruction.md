# DAC Restore 6bit 1p8

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_restore_6bit_1p8.va`: `dac_restore_6bit_1p8`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_EACH_RISING_CROSSING_OF_CLK`: On each rising crossing of `clk` through `vth`, sample `d1..d6` and decode an unsigned 6-bit code with weights `32, 16, 8, 4, 2, 1`. Hold the decoded output until the next rising clock event. Map the sampled code to a bipolar 1.8 V mid-rise level:
- `P_TEXT_VOUT_CODE_0_5_3`: ```text vout = (code + 0.5) * 3.6 / 64 - 1.8 ```
- `P_THE_ALL_ZERO_CODE_THEREFORE_PRODUCES`: The all-zero code therefore produces the lowest half-LSB-centered negative level, and the all-one code produces the highest half-LSB-centered positive level.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_restore_6bit_1p8.va`.
Do not add or omit artifacts.
