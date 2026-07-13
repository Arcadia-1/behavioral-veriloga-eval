# Dither Noise Like Deterministic Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `noise_gen_ref.va`: `noise_gen`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PERIODIC_UPDATE`: The deterministic perturbation sample updates once every dt seconds.
- `P_SAMPLE_HOLD`: Between update events, the perturbation vout_o minus vin_i remains piecewise constant.
- `P_ADDITIVE_OUTPUT`: At all times after the first update, vout_o equals vin_i plus sigma times the currently held normalized perturbation sample.
- `P_DETERMINISTIC_SEQUENCE`: The normalized perturbation sample repeats the public eight-sample sequence [-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5], advancing by one entry at each dt update.
- `P_ZERO_MEAN_DITHER`: Every complete eight-sample sequence period is exactly zero mean, and every perturbation is bounded within [-sigma, +sigma].

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `noise_gen_ref.va`.
Do not add or omit artifacts.
