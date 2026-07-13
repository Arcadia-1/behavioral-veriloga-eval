# Converter Static Linearity Measurement Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Converter Static Linearity Measurement` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_STATE`: Active-high reset clears the retained conversion and previous-step state to the public reset values.
- `P_FOUR_BIT_QUANTIZATION`: On each non-reset rising clk edge, vin clips to 0 through vfs and quantizes monotonically to one of 16 codes represented as code_index times vfs/15.
- `P_PUBLIC_RECONSTRUCTION_TABLE`: For each code 0 through 15, recon equals the corresponding value in the public monotonic non-ideal reconstruction table, with default table voltages scaled by vfs/0.9 for legal vfs overrides.
- `P_INL_METRIC`: INL encodes reconstruction error from the vfs/15-per-code ideal ramp using the public gain and 0.05 V through 0.85 V clamp.
- `P_DNL_INCREASING_STEP`: For a valid increasing code step, dnl encodes actual reconstruction-step error relative to vfs/15 per code step with the public scaling and clamp.
- `P_DNL_NO_STEP_BASELINE`: Before a valid increasing step, or when code does not increase, dnl is held at the 0.45 V baseline.

The required trace names are: `time`, `clk`, `rst`, `vin`, `code`, `recon`, `dnl`, `inl`.

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
