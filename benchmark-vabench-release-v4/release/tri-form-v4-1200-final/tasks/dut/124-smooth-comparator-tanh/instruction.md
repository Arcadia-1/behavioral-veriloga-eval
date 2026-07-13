# Smooth Comparator Tanh

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `smooth_comparator_tanh.va`: `smooth_comparator_tanh`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TANH_TRANSFER`: Drive `sigout` as `0.5 * (high - low) * tanh(comp_slope * (V(sigin, sigref) - offset)) + 0.5 * (high + low)`.
- `P_INPUT_POLARITY`: A larger `V(sigin, sigref)` must move the output toward `high`, not toward `low`.
- `P_SMOOTH_TRANSITION`: The output must transition smoothly between `low` and `high` according to the tanh slope, not as a hard switch.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `smooth_comparator_tanh.va`.
Do not add or omit artifacts.
