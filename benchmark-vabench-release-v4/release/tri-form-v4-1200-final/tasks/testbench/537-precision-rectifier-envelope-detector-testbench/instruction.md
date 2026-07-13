# Precision Rectifier Envelope Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Precision Rectifier Envelope Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_FULL_WAVE_RECTIFICATION`: Rect equals vcm plus the absolute input deviation from vcm, so equal positive and negative excursions produce equal rectified levels, bounded to 0 V through 0.9 V.
- `P_RESET_ENVELOPE`: Initialization or a rising clk update with rst active restores env to vcm and clears envelope memory.
- `P_PEAK_ATTACK`: At a rising clk update, a rectified value above the stored envelope is acquired immediately as the new env value.
- `P_BOUNDED_DECAY`: When rect is below the stored envelope, each rising clk update lowers env by at most decay and never below rect or vcm.
- `P_ENVELOPE_LAG_METRIC`: Metric is high while env exceeds rect by more than 30 mV and low otherwise.

The required trace names are: `time`, `clk`, `rst`, `vin`, `rect`, `env`, `metric`.

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
