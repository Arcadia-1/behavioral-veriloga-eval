# SAR 13bit Serial Decoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SAR 13bit Serial Decoder` DUT. The evaluator runs the same submitted bytes
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

- `P_CONSUME_ONE_MSB_FIRST_BIT_ON`: Consume one MSB-first bit on each rising `ready` crossing, starting with bit 12 and ending with bit 0.
- `P_ADD_THE_CORRESPONDING_BINARY_WEIGHT_WHEN`: Add the corresponding binary weight when `din` is high.
- `P_INCREMENT_DNUM_FOR_EACH_HIGH_DECISION`: Increment `dnum` for each high decision in the current frame.
- `P_ON_EACH_RISING_CLKS_CROSSING_PUBLISH`: On each rising `clks` crossing, publish the previous frame as a normalized bipolar output.
- `P_MAP_AN_ALL_LOW_FRAME_TO`: Map an all-low frame to `-0.5` and an all-high frame near `+0.5`.
- `P_AFTER_PUBLISHING_RESET_THE_ACCUMULATOR_HIGH`: After publishing, reset the accumulator, high-bit count, and bit pointer for the next frame.

The required trace names are: `time`, `din`, `clks`, `ready`, `dout`, `dnum`.

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
