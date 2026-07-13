# Pipe15 Data Align

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pipe15_data_align.va`: `pipe15_data_align`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAMPLE_ON_RISING_SAMP`: On each rising `samp` crossing, sample all fifteen input bits `d0..d14` into the alignment pipeline.
- `P_ZERO_DELAY_OUTPUT_GROUP`: Outputs `do0..do2` publish the current sampled values without an added sample delay.
- `P_STAGGERED_DELAY_OUTPUT_GROUPS`: Outputs `do3..do6`, `do7..do10`, and `do11..do14` publish the one-, two-, and three-sample delayed input groups respectively.
- `P_VOLTAGE_CODED_OUTPUT_LEVELS`: Every aligned output is driven as a voltage-coded logic level near 0 V or `vdd` with the declared transition timing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pipe15_data_align.va`.
Do not add or omit artifacts.
