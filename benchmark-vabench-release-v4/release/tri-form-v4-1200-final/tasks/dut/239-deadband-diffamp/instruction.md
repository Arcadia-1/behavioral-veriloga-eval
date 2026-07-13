# Deadband Diffamp

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `deadband_diffamp.va`: `deadband_diffamp`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_POLARITY`: Compute the differential input as `V(sigin_p, sigin_n)` with the documented polarity.
- `P_DEADBAND_LEAK_OUTPUT`: Inside the inclusive differential deadband, drive the public leakage level `sigout_leak`.
- `P_ASYMMETRIC_RESIDUE_GAINS`: Below the lower threshold use `gain_low` for the low-side signed residue plus leakage; above the upper threshold use `gain_high` for the high-side signed residue plus leakage.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `deadband_diffamp.va`.
Do not add or omit artifacts.
