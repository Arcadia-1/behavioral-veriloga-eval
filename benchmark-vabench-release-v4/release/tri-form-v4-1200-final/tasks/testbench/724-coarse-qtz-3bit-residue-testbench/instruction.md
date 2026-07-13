# Coarse QTZ 3bit Residue Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Coarse QTZ 3bit Residue` DUT. The evaluator runs the same submitted bytes
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

- `P_CLIP_VIN_TO_THE_RANGE_FROM`: Clip `vin` to the range from `-vref` to `+vref`.
- `P_QUANTIZE_THE_CLIPPED_VALUE_INTO_EIGHT`: Quantize the clipped value into eight 3-bit codes using round-to-nearest behavior.
- `P_SATURATE_THE_CODE_AT_THE_ENDPOINTS`: Saturate the code at the endpoints.
- `P_USE_UNIFORMLY_SPACED_QUANTIZATION_LEVELS_START`: Use uniformly spaced quantization levels starting at `-vref`, with one LSB equal to one eighth of the full input span.
- `P_DRIVE_D0_D1_AND_D2_AS`: Drive `d0`, `d1`, and `d2` as LSB-to-MSB voltage-coded bits.
- `P_DRIVE_VRES_AS_THE_CLIPPED_INPUT`: Drive `vres` as the clipped input minus the selected quantized analog level.

The required trace names are: `time`, `vin`, `d0`, `d1`, `d2`, `vres`.

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
