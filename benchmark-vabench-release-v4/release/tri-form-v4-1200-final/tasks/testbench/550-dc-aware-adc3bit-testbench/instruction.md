# DC Aware ADC3bit Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DC Aware ADC3bit` DUT. The evaluator runs the same submitted bytes
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

- `P_STATIC_CONVERSION`: The output code represents the current vin level without requiring a clock or prior transient event.
- `P_UNIFORM_QUANTIZATION`: The 0-to-vref input span is divided into eight ordered uniform code regions producing unsigned codes 0 through 7.
- `P_INPUT_CLIPPING`: Inputs at or below 0 V produce code 0, and inputs at or above vref produce code 7.
- `P_BINARY_BIT_ORDER`: d2 is the most significant output bit and d0 is the least significant output bit.
- `P_OUTPUT_LEVELS`: Each output bit approaches 0 V for logic low and vh for logic high with finite transition smoothing.

The required trace names are: `time`, `vin`, `d2`, `d1`, `d0`.

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
