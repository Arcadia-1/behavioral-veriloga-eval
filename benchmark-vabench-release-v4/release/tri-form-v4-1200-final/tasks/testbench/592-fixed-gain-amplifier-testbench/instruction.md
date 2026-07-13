# Fixed Gain Amplifier Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Fixed Gain Amplifier` DUT. The evaluator runs the same submitted bytes
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

- `P_DIFFERENTIAL_GAIN`: The output differential equals ACTUAL_GAIN times the input differential.
- `P_POSITIVE_POLARITY`: A positive input differential produces a positive output differential and a negative input differential produces a negative output differential.
- `P_OUTPUT_COMMON_MODE`: The output pair remains centered at vdd/2 independently of input common mode.
- `P_SYMMETRIC_OUTPUT_PAIR`: Half the amplified differential is added to VOUT_P and half is subtracted from VOUT_N.
- `P_PARAMETER_OVERRIDES`: Legal ACTUAL_GAIN and vdd overrides alter differential gain and output common mode according to their declared meanings.

The required trace names are: `time`, `vin_p`, `vin_n`, `vout_p`, `vout_n`.

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
