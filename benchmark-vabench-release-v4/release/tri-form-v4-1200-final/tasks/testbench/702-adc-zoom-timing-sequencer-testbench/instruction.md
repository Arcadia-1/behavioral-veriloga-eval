# ADC Zoom Timing Sequencer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `ADC Zoom Timing Sequencer` DUT. The evaluator runs the same submitted bytes
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

- `P_GENERATE_A_REPEATING_32_NS_COMPACT`: Generate a repeating 32 ns compact ADC timing frame with these high windows: `rst` from 0.5 to 0.8 ns; `s` from 1.5 to 2.5 ns; `sar` from 3.0 to 5.4 ns; `clk_sar` from 3.0 to 3.25 ns, 3.6 to 3.85 ns, and 4.2 to 4.45 ns; `res` from 6.0 to 6.6 ns; `intg` from 8.0 to 8.7 ns; `zoom` from 9.2 to 10.8 ns; `clk_zoom` from 9.2 to 9.45 ns and 9.8 to 10.05 ns; and `rst_zoom` from 11.0 to 11.5 ns. All outputs should return low between their public windows and repeat every 32 ns.

The required trace names are: `time`, `rst`, `s`, `sar`, `res`, `intg`, `clk_sar`, `zoom`, `clk_zoom`, `rst_zoom`.

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
