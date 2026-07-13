# Samplehold Rising Edge Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Samplehold Rising Edge` DUT. The evaluator runs the same submitted bytes
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

- `P_SAMPLE_VIN_ON_EACH_RISING_CONTROL`: Sample `vin` on each rising `control` crossing of `thresh`.
- `P_HOLD_THE_SAMPLED_VOLTAGE_ON_VOUT`: Hold the sampled voltage on `vout` until the next rising control crossing.
- `P_DO_NOT_CONTINUOUSLY_TRACK_VIN_BETWEEN`: Do not continuously track `vin` between sample events.
- `P_DRIVE_VOUT_WITH_SMOOTH_VOLTAGE_DOMAIN`: Drive `vout` with smooth voltage-domain output behavior.

The required trace names are: `time`, `control`, `vin`, `vout`.

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
