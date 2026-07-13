# Onehot Progress Encoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `onehot_progress_encoder.va`: `onehot_progress_encoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PROGRESS_INITIAL_STATE`: All progress outputs and the count initialize to zero.
- `P_SEQUENTIAL_ONEHOT_ASSERTION`: Each rising `ck` crossing asserts the next progress bit in order from `d0` through `d15` without skipping the first bit.
- `P_ACCUMULATING_PROGRESS_BITS`: Previously asserted progress bits remain high until all sixteen bits have been asserted.
- `P_SUM_COUNT_OUTPUT`: `sum` reports the current count value corresponding to the number of asserted progress bits.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `onehot_progress_encoder.va`.
Do not add or omit artifacts.
