# Bipolar DAC 4b Continuous Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bipolar DAC 4b Continuous` DUT. The evaluator runs the same submitted bytes
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

- `P_UNSIGNED_BIT_DECODE`: Each input is decoded continuously as one only when its voltage exceeds vtrans, with vd3 as MSB and vd0 as LSB.
- `P_NEGATIVE_FULL_SCALE`: Unsigned code 0 produces approximately negative vref.
- `P_POSITIVE_FULL_SCALE`: Unsigned code 15 produces approximately positive vref.
- `P_UNIFORM_CODE_STEP`: Every one-code increase raises the output target by the same voltage increment across codes 0 through 15.
- `P_MONOTONIC_TRANSFER`: The output is strictly monotonic with increasing unsigned code for vref greater than zero.
- `P_CONTINUOUS_REEVALUATION`: The DAC target responds to input-code threshold changes without requiring a clock event, using tdel, trise, and tfall for output timing.

The required trace names are: `time`, `vd3`, `vd2`, `vd1`, `vd0`, `vout`.

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
