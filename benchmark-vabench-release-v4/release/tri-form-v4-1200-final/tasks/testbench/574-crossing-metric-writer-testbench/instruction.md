# Crossing Metric Writer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Crossing Metric Writer` DUT. The evaluator runs the same submitted bytes
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

- `P_FILE_OPEN`: The filename parameter names exactly one metric file basename in the runner-provided writable working directory; absolute paths and directory traversal are outside the public contract.
- `P_FIRST_RISING_CROSSING`: The first rising crossing of vin through vth is the event that records the metric and latches completion.
- `P_RECORDED_TIME`: The metric file contains exactly one text record of the form `cross <time_seconds>` followed by a newline, where <time_seconds> is the first rising crossing time.
- `P_DONE_LATCH`: done remains low before the first qualifying crossing and high after it, with transition smoothing set by tr.
- `P_SINGLE_RECORD`: Later vin crossings do not clear done or create additional metric records.

The required trace names are: `time`, `vin`, `done`.

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
