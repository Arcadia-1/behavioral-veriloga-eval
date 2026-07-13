# Clocked Mux4 Sampler Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked Mux4 Sampler` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_SELECTS_DIN0`: While `rst` is high, the selected channel and `dout` are forced to `din0`.
- `P_FALLING_CLOCK_UPDATE_SAMPLE`: On each falling `clks` crossing with reset inactive and `update` high, latch `dsel0/dsel1` and sample the selected input.
- `P_UPDATE_LOW_HOLDS_STATE`: On falling `clks` crossings with `update` low, hold the previous selection and output value.
- `P_SELECT_DECODE_AND_OUTPUT_TIMING`: The held two-bit selection maps to `din0..din3` in binary order and drives `dout` with the declared transition timing.

The required trace names are: `time`, `clks`, `din0`, `din1`, `din2`, `din3`, `dout`, `dsel0`, `dsel1`, `rst`, `update`.

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
