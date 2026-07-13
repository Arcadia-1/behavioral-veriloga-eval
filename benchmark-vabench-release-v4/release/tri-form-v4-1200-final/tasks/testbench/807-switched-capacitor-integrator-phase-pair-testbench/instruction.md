# Switched-capacitor Integrator Phase Pair Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Switched-capacitor Integrator Phase Pair` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear the integration state, drive `vout` to `vcm`, and clear `valid`.
- `P_ON_A_RISING_PHI1_CROSSING_SAMPLE`: On a rising `phi1` crossing, sample the input deviation from `vcm` into the sampling state.
- `P_ON_THE_FOLLOWING_RISING_PHI2_CROSSING`: On the following rising `phi2` crossing, add `k_int` times the sampled deviation to the integrator state.
- `P_REJECT_OVERLAPPING_PHI1_AND_PHI2_UPDATES`: Reject overlapping `phi1` and `phi2` updates by holding the previous state and lowering `valid` for that cycle.
- `P_EXPOSE_THE_MOST_RECENT_ACCEPTED_PHASE`: Expose the most recent accepted phase pair on `phase_metric` and clamp `vout` to the rails.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin`, `phi1`, `phi2`, `rst`, `enable`, `vout`, `phase_metric`, `valid`.

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
