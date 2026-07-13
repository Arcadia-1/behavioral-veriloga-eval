# First Order Lowpass Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `first_order_lowpass.va`: `first_order_lowpass`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_STATE`: vout begins at 0 V before the first periodic update.
- `P_PERIODIC_UPDATE`: The internal output updates only on the public 500 ps periodic schedule using y := y + alpha*(vin-y).
- `P_STEP_MONOTONICITY`: For a positive input step, vout is monotone and bounded by the input level.
- `P_LOW_PASS_RESPONSE`: The step response is slower than an instantaneous copy of vin.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `first_order_lowpass.va`.
Every supplied `.va` file is editable; do not add or omit files.
