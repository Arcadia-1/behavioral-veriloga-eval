# Smooth Limiting Diffamp

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `limiting_diffamp.va`: `limiting_diffamp`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ODD_DIFFERENTIAL_POLARITY`: Compute `V(sigin_p, sigin_n)`, preserve polarity, and drive an odd differential transfer.
- `P_SMALL_SIGNAL_GAIN`: Near zero differential input, drive approximately `gain * V(sigin_p, sigin_n)`.
- `P_SMOOTH_SYMMETRIC_LIMITING`: For large positive and negative differential inputs, smoothly approach `+limit` and `-limit` without a hard clamp.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `limiting_diffamp.va`.
Do not add or omit artifacts.
