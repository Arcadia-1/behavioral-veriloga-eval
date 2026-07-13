# Bipolar DAC 4b Continuous

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bipolar_dac_4b_continuous.va`: `bipolar_dac_4b_continuous`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_UNSIGNED_BIT_DECODE`: Each input is decoded continuously as one only when its voltage exceeds vtrans, with vd3 as MSB and vd0 as LSB.
- `P_NEGATIVE_FULL_SCALE`: Unsigned code 0 produces approximately negative vref.
- `P_POSITIVE_FULL_SCALE`: Unsigned code 15 produces approximately positive vref.
- `P_UNIFORM_CODE_STEP`: Every one-code increase raises the output target by the same voltage increment across codes 0 through 15.
- `P_MONOTONIC_TRANSFER`: The output is strictly monotonic with increasing unsigned code for vref greater than zero.
- `P_CONTINUOUS_REEVALUATION`: The DAC target responds to input-code threshold changes without requiring a clock event, using tdel, trise, and tfall for output timing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bipolar_dac_4b_continuous.va`.
Do not add or omit artifacts.
