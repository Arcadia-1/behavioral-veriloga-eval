# Config Shift Register 64b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `config_shift_reg_64b.va`: `config_shift_reg_64b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ACTIVE_LOW_RESET`: On a rising clock crossing with rst_n low, every q bit is cleared to logic low.
- `P_SERIAL_SHIFT_DIRECTION`: On each rising clock crossing with rst_n high, serial_in enters q[0], previous q[N] moves to q[N+1], and previous q[62] moves to q[63].
- `P_ONE_SHIFT_PER_EDGE`: Exactly one register-position shift occurs for each qualifying rising clock crossing.
- `P_HOLD_BETWEEN_EDGES`: The parallel register state holds between rising clock crossings despite changes on serial_in.
- `P_OUTPUT_LEVELS`: Each q bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `config_shift_reg_64b.va`.
Every supplied `.va` file is editable; do not add or omit files.
