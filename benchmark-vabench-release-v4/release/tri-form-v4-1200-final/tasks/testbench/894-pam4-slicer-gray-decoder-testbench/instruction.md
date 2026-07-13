# PAM4 Slicer and Gray Decoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PAM4 Slicer and Gray Decoder` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears both bits, level metric, and valid.
- `P_RISING_EDGE_SAMPLE_HOLD`: vin is sliced only on enabled rising clk edges and outputs hold between samples.
- `P_PAM4_THRESHOLDS`: The three ordered thresholds divide vin into levels zero through three.
- `P_GRAY_MAPPING`: Levels zero through three map to Gray codes 00, 01, 11, and 10.
- `P_LEVEL_METRIC`: level_metric reports the sliced level as vss plus k/3 of the output span.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `bit_msb`, `bit_lsb`, `level_metric`, `valid`.

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
