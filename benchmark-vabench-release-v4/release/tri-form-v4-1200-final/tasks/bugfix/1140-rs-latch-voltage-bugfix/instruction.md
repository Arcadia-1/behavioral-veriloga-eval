# RS Latch Voltage Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `rs_latch_voltage.va`: `rs_latch_voltage`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_LOGIC_THRESHOLDS_OUTPUT_AMPLITUDE`: Interpret set and reset as logic high above 0.45 V and drive outputs with 0.9 V high and 0.0 V low levels.
- `P_SET_RESET_PRIORITY`: A set-only input drives Q high, and a reset-only input drives Q low.
- `P_HOLD_STATE`: When neither set-only nor reset-only is asserted, preserve the previous Q state after initializing Q low.
- `P_QBAR_COMPLEMENT`: Drive `vout_qbar` as the logical complement of Q.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `rs_latch_voltage.va`.
Every supplied `.va` file is editable; do not add or omit files.
