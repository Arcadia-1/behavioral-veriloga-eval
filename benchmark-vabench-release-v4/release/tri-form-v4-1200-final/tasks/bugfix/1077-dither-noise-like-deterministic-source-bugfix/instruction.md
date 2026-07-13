# Dither Noise Like Deterministic Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `noise_gen_ref.va`: `noise_gen`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PERIODIC_UPDATE`: The deterministic perturbation sample updates once every dt seconds.
- `P_SAMPLE_HOLD`: Between update events, the perturbation vout_o minus vin_i remains piecewise constant.
- `P_ADDITIVE_OUTPUT`: At all times after the first update, vout_o equals vin_i plus sigma times the currently held normalized perturbation sample.
- `P_DETERMINISTIC_SEQUENCE`: The normalized perturbation sample repeats the public eight-sample sequence [-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5], advancing by one entry at each dt update.
- `P_ZERO_MEAN_DITHER`: Every complete eight-sample sequence period is exactly zero mean, and every perturbation is bounded within [-sigma, +sigma].

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `noise_gen_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
