# Pipe15 Data Align Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Pipe15 Data Align` DUT. The evaluator runs the same submitted bytes
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

- `P_SAMPLE_ON_RISING_SAMP`: On each rising `samp` crossing, sample all fifteen input bits `d0..d14` into the alignment pipeline.
- `P_ZERO_DELAY_OUTPUT_GROUP`: Outputs `do0..do2` publish the current sampled values without an added sample delay.
- `P_STAGGERED_DELAY_OUTPUT_GROUPS`: Outputs `do3..do6`, `do7..do10`, and `do11..do14` publish the one-, two-, and three-sample delayed input groups respectively.
- `P_VOLTAGE_CODED_OUTPUT_LEVELS`: Every aligned output is driven as a voltage-coded logic level near 0 V or `vdd` with the declared transition timing.

The required trace names are: `time`, `d0`, `d1`, `d10`, `d11`, `d12`, `d13`, `d14`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`, `do0`, `do1`, `do10`, `do11`, `do12`, `do13`, `do14`, `do2`, `do3`, `do4`, `do5`, `do6`, `do7`, `do8`, `do9`, `samp`.

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
