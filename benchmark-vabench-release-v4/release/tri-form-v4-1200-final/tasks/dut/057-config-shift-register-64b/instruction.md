# Config Shift Register 64b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `config_shift_reg_64b.va`: `config_shift_reg_64b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ACTIVE_LOW_RESET`: On a rising clock crossing with rst_n low, every q bit is cleared to logic low.
- `P_SERIAL_SHIFT_DIRECTION`: On each rising clock crossing with rst_n high, serial_in enters q[0], previous q[N] moves to q[N+1], and previous q[62] moves to q[63].
- `P_ONE_SHIFT_PER_EDGE`: Exactly one register-position shift occurs for each qualifying rising clock crossing.
- `P_HOLD_BETWEEN_EDGES`: The parallel register state holds between rising clock crossings despite changes on serial_in.
- `P_OUTPUT_LEVELS`: Each q bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `config_shift_reg_64b.va`.
Do not add or omit artifacts.
