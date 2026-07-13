# Linear PFD Gain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `linear_pfd_gain.va`: `linear_pfd_gain`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_INPUT_POLARITY`: `out` uses the input difference `in1 - in2`, preserving the specified differential polarity.
- `P_KPHI_GAIN_SCALE`: `out` is scaled by the public gain coefficient `kphi` rather than unit gain or an alternate scale.
- `P_CONTINUOUS_ANALOG_TRACKING`: `out` continuously tracks analog input changes without clocked state, clipping, or single-ended substitution.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `linear_pfd_gain.va`.
Do not add or omit artifacts.
