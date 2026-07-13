# Correlated Double Sampler Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Correlated Double Sampler` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_SAMPLE`: A rising phi_reset crossing captures vin as the reset level, returns vout to vcm, and clears valid.
- `P_SIGNAL_CORRECTION`: A rising phi_signal crossing publishes vcm plus gain times the current signal sample minus the most recently captured reset sample.
- `P_OUTPUT_CLAMP`: The corrected output is limited to the inclusive vlo-to-vhi range.
- `P_VALID_SEQUENCE`: valid is low before a completed signal sample and after every reset sample, then rises to vhi when a signal sample is published.
- `P_HOLD_BETWEEN_EVENTS`: vout and valid hold their last event-updated states between reset and signal sampling crossings.

The required trace names are: `time`, `phi_reset`, `phi_signal`, `vin`, `vout`, `valid`.

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
