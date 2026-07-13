# Sync 8b DFFs V2

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sync_8b_dffs_v2.va`: `sync_8b_dffs_v2`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PHASED_CAPTURE_ORDER`: Each phase clock captures its corresponding `dl` input and shifts previously captured upper-phase data down the chain in the specified order.
- `P_INTERMEDIATE_OUTPUT_CAPTURE`: Intermediate outputs, including `do4`, reflect their synchronized pipeline state rather than a stuck or skipped stage.
- `P_FINAL_OUTPUT_CAPTURE`: The most delayed output `do8` reflects the final synchronized stage with correct polarity.
- `P_FULL_LEVEL_OUTPUTS`: All `do` outputs drive full voltage-coded levels for their captured state.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sync_8b_dffs_v2.va`.
Do not add or omit artifacts.
