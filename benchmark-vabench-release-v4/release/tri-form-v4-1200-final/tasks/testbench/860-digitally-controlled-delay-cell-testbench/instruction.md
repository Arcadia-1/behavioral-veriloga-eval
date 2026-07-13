# Digitally Controlled Delay Cell Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Digitally Controlled Delay Cell` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEAR`: Reset clears the loaded code state, delayed clock, delay metric, valid indication, and pending edges.
- `P_CODE_CAPTURE_METRIC`: A rising load edge captures the six-bit unsigned code and the delay metric reports the normalized captured code.
- `P_EDGE_DELAY_MAPPING`: Each input-clock edge appears at the output after delay_min plus delay_lsb times the code captured for that edge.
- `P_PULSE_INTEGRITY_VALID`: Rising and falling edges receive equal delay, preserving pulse width, and valid asserts after the first delayed rising edge.

The required trace names are: `time`, `in_clk`, `load`, `rst`, `code_5`, `code_4`, `code_3`, `code_2`, `code_1`, `code_0`, `out_clk`, `delay_metric`, `valid`.

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
