# Onehot Progress Encoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `onehot_progress_encoder.va`: `onehot_progress_encoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PROGRESS_INITIAL_STATE`: All progress outputs and the count initialize to zero.
- `P_SEQUENTIAL_ONEHOT_ASSERTION`: Each rising `ck` crossing asserts the next progress bit in order from `d0` through `d15` without skipping the first bit.
- `P_ACCUMULATING_PROGRESS_BITS`: Previously asserted progress bits remain high until all sixteen bits have been asserted.
- `P_SUM_COUNT_OUTPUT`: `sum` reports the current count value corresponding to the number of asserted progress bits.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `onehot_progress_encoder.va`.
Every supplied `.va` file is editable; do not add or omit files.
