# Windowed Event Rate Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Windowed Event Rate Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIALIZE_EVENT_COUNT_SAMPLE_COUNT_RATE`: Initialize `event_count`, `sample_count`, `rate`, and `average` to zero. On each rising clock crossing, clear the measurement window and both observables when `rst` is high or `gate <= vth`. Otherwise increment `sample_count`, increment `event_count` when `event_in > vth`, and drive `rate = vhi * clip01(event_count / window_count)`.
- `P_FOR_THE_SAME_GATED_SAMPLE_WINDOW`: For the same gated sample window, drive `average = vhi * clip01(event_count / sample_count)`. Hold the last observable values between rising clock crossings.

The required trace names are: `time`, `clk`, `rst`, `event_in`, `gate`, `rate`, `average`.

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
