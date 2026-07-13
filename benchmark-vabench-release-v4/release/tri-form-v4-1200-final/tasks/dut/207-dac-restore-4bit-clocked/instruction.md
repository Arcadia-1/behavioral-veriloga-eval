# DAC Restore 4bit Clocked

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_restore_4bit_clocked.va`: `dac_restore_4bit_clocked`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_EACH_RISING_CLK_CROSSING_DECODE`: On each rising `clk` crossing, decode `d3..d0` as a 4-bit binary word and drive `vout` to the center of that code bin across a bipolar 1.8 V span from `-0.9 V` to `+0.9 V`. Hold the output between clock events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_restore_4bit_clocked.va`.
Do not add or omit artifacts.
