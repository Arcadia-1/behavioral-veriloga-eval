# Multi-channel Sample/Mux/Readout Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Multi-channel Sample/Mux/Readout` DUT. The evaluator runs the same submitted bytes
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

- `P_READOUT_RESET_CLEAR`: Reset clears held channels, selector, out, and valid.
- `P_READOUT_SIMULTANEOUS_SAMPLE`: An enabled rising clock captures all four input channels into one coherent held bank.
- `P_READOUT_CHANNEL_ORDER`: Read cycles select held channels in order zero, one, two, three and wrap.
- `P_READOUT_HELD_VALUE`: out equals the held value of the exposed selected channel, independent of later live-input changes.
- `P_READOUT_VALID_TIMING`: valid is high only for read cycles; when read is low out holds and the pointer does not advance.

The required trace names are: `time`, `ch0`, `ch1`, `ch2`, `ch3`, `clk`, `rst`, `sample`, `read`, `out`, `ch_sel_1`, `ch_sel_0`, `valid`.

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
