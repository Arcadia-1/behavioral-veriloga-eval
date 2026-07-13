# Deadband Window

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `deadband_window.va`: `deadband_window`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ZERO_INSIDE_DEADBAND`: For `dead_low <= V(sigin) <= dead_high`, drive `sigout` to 0 V.
- `P_LOWER_RESIDUE`: For `V(sigin) < dead_low`, drive `sigout` to `V(sigin) - dead_low`.
- `P_UPPER_RESIDUE`: For `V(sigin) > dead_high`, drive `sigout` to `V(sigin) - dead_high`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `deadband_window.va`.
Do not add or omit artifacts.
