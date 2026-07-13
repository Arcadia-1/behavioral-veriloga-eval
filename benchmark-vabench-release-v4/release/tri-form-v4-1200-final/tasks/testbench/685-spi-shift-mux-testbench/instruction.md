# SPI Shift Mux Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SPI Shift Mux` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_LOADS_DEFAULT_WORD`: Initialization and active-high `rst` load the 8-bit word `10110010` with `out7` as the leftmost bit and `out0` as the rightmost bit.
- `P_SHIFT_ON_SCKI_TRANSITIONS`: While reset is inactive, every `scki` transition shifts the register exactly once.
- `P_SHIFT_DIRECTION_AND_SDI_INSERTION`: The shift moves bits toward higher output indexes and inserts `sdi` into the declared end of the register.
- `P_SDO_EXPOSES_SHIFTED_OUT_BIT`: `sdo` exposes the shifted-out `out7` bit rather than another register bit.
- `P_OUTPUT_RAIL_LEVELS`: The parallel outputs and `sdo` are voltage-coded at valid low/high levels.

The required trace names are: `time`, `out0`, `out1`, `out2`, `out3`, `out4`, `out5`, `out6`, `out7`, `rst`, `scki`, `scko`, `sdi`, `sdo`.

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
