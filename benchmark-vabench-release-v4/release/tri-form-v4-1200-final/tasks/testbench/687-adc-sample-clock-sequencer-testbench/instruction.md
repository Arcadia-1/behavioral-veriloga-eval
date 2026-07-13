# ADC Sample Clock Sequencer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `ADC Sample Clock Sequencer` DUT. The evaluator runs the same submitted bytes
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

- `P_PERIODIC_18NS_FRAME`: Generate a repeating 18 ns timing frame.
- `P_RESET_SAMPLE_AND_SS_WINDOWS`: `rst`, `s`, and `ss` are high only in the declared frame windows.
- `P_NONOVERLAP_AND_AUTOZERO_WINDOWS`: `nc` and `nc_az` use the declared non-overlap and autozero windows without swapping outputs.
- `P_CONVERSION_WINDOW_TIMING`: `conv` is asserted in the declared conversion windows with the correct phase.
- `P_TIMING_OUTPUT_LEVELS`: All timing outputs drive valid voltage-coded low/high levels.

The required trace names are: `time`, `conv`, `nc`, `nc_az`, `rst`, `s`, `ss`.

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
