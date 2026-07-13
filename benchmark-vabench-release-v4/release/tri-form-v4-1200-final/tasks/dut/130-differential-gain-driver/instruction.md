# Differential Gain Driver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `differential_gain_driver.va`: `differential_gain_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_INPUT_GAIN`: Read `V(sigin_p, sigin_n)` and multiply it by the overridable `gain` parameter.
- `P_BALANCED_HALF_SPLIT`: Drive `sigout_p` and `sigout_n` as equal and opposite half-swings around `sigref`.
- `P_OUTPUT_POLARITY`: For a positive input differential, `sigout_p` rises relative to `sigref` and `sigout_n` falls relative to `sigref`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `differential_gain_driver.va`.
Do not add or omit artifacts.
