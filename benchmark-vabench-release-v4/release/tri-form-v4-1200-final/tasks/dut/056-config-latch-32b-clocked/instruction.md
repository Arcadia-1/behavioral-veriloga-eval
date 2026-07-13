# Config Latch 32b Clocked

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `config_latch_32b.va`: `config_latch_32b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ENABLED_PASS`: When en is high, every q bit equals the corresponding voltage-coded d bit.
- `P_DISABLED_CLEAR`: When en is low, every q bit is driven low regardless of the data input.
- `P_STATIC_ENABLE_BEHAVIOR`: The public interface is combinational enable gating: q follows data changes while enabled and does not retain a prior word while disabled.
- `P_BIT_ALIGNMENT`: Each d[N] controls only the same-index q[N]; bus order is not reversed or shifted.
- `P_OUTPUT_LEVELS`: Each q bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `config_latch_32b.va`.
Do not add or omit artifacts.
