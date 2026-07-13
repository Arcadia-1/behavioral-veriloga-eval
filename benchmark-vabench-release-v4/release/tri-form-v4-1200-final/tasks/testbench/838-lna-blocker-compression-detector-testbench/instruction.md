# LNA Blocker Compression Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LNA Blocker Compression Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive output to `vcm` and clear compression outputs.
- `P_AMPLIFY_VIN_VCM_WITH_SMALL_SIGNAL`: Amplify `vin - vcm` with small-signal gain when `blocker` is low.
- `P_REDUCE_EFFECTIVE_GAIN_AS_BLOCKER_RISES`: Reduce effective gain as `blocker` rises above `blocker_start`.
- `P_EXPOSE_GAIN_REDUCTION_ON_COMPRESSION_METRIC`: Expose gain reduction on `compression_metric`.
- `P_ASSERT_COMPRESSED_ONLY_WHEN_THE_EFFECTIVE`: Assert `compressed` only when the effective gain is reduced by more than `compression_tol`.

The required trace names are: `time`, `vin`, `blocker`, `enable`, `rst`, `vout`, `compression_metric`, `compressed`.

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
