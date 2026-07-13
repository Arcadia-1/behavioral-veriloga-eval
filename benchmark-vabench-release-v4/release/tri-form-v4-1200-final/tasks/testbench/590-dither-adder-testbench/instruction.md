# Dither Adder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Dither Adder` DUT. The evaluator runs the same submitted bytes
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

- `P_POSITIVE_DITHER`: When DPN is above vth, the output differential exceeds the input differential by DITHER_AMP.
- `P_NEGATIVE_DITHER`: When DPN is at or below vth, the output differential is lower than the input differential by DITHER_AMP.
- `P_SYMMETRIC_SPLIT`: Half of the selected differential dither is added to VOUT_P and half is subtracted from VOUT_N.
- `P_COMMON_MODE_PRESERVATION`: The output pair preserves the input common mode and does not introduce a vdd/2 offset.
- `P_PARAMETER_OVERRIDE`: Legal DITHER_AMP and vth overrides change only dither magnitude and polarity decision as declared.

The required trace names are: `time`, `vres_p`, `vres_n`, `dpn`, `vout_p`, `vout_n`.

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
