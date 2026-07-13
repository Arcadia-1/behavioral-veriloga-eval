# Dither Noise Like Deterministic Source Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Dither Noise Like Deterministic Source` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_PERIODIC_UPDATE`: The deterministic perturbation sample updates once every dt seconds.
- `P_SAMPLE_HOLD`: Between update events, the perturbation vout_o minus vin_i remains piecewise constant.
- `P_ADDITIVE_OUTPUT`: At all times after the first update, vout_o equals vin_i plus sigma times the currently held normalized perturbation sample.
- `P_DETERMINISTIC_SEQUENCE`: The normalized perturbation sample repeats the public eight-sample sequence [-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5], advancing by one entry at each dt update.
- `P_ZERO_MEAN_DITHER`: Every complete eight-sample sequence period is exactly zero mean, and every perturbation is bounded within [-sigma, +sigma].

The required trace names are: `time`, `vin_i`, `vout_o`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
