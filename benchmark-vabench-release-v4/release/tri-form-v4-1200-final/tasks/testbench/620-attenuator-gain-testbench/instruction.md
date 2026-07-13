# Attenuator Gain Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Attenuator Gain` DUT. The evaluator runs the same submitted bytes
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

- `P_ZERO_DB_UNITY`: With attenuation set to 0 dB, vout continuously equals vin.
- `P_DB_AMPLITUDE_RATIO`: For positive attenuation, the vout-to-vin amplitude ratio follows the standard voltage decibel attenuation relationship.
- `P_POLARITY_PRESERVATION`: The attenuator preserves input polarity and introduces no inversion or offset.
- `P_MONOTONIC_ATTENUATION`: For a fixed nonzero vin magnitude, increasing the nonnegative attenuation parameter cannot increase the magnitude of vout.
- `P_CONTINUOUS_RESPONSE`: vout is a continuous memoryless scaled version of vin without clocking, retained state, clipping, or added delay.

The required trace names are: `time`, `vin`, `vout`.

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
