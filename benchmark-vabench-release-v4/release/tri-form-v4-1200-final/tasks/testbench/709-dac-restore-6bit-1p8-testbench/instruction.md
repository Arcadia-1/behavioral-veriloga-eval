# DAC Restore 6bit 1p8 Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DAC Restore 6bit 1p8` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_EACH_RISING_CROSSING_OF_CLK`: On each rising crossing of `clk` through `vth`, sample `d1..d6` and decode an unsigned 6-bit code with weights `32, 16, 8, 4, 2, 1`. Hold the decoded output until the next rising clock event. Map the sampled code to a bipolar 1.8 V mid-rise level:
- `P_TEXT_VOUT_CODE_0_5_3`: ```text vout = (code + 0.5) * 3.6 / 64 - 1.8 ```
- `P_THE_ALL_ZERO_CODE_THEREFORE_PRODUCES`: The all-zero code therefore produces the lowest half-LSB-centered negative level, and the all-one code produces the highest half-LSB-centered positive level.

The required trace names are: `time`, `clk`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `vout`.

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
