# Deadband Voltage

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `deadband_voltage.va`: `deadband_voltage`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DEADBAND_ZERO_REGION`: Inside the inclusive deadband window from `sigin_dead_low` to `sigin_dead_high`, drive `sigout` to `0 V`.
- `P_SIGNED_RESIDUE_OUTSIDE_WINDOW`: Below the lower edge, drive the signed excess below `sigin_dead_low`; above the upper edge, drive the signed excess above `sigin_dead_high` while preserving sign.
- `P_DEADBAND_EDGE_CONTINUITY`: Use the public lower and upper threshold values so the output is continuous at both deadband edges.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `deadband_voltage.va`.
Do not add or omit artifacts.
