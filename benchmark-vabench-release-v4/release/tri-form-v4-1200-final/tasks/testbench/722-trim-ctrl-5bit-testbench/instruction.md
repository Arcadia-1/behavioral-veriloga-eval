# Trim Ctrl 5bit Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Trim Ctrl 5bit` DUT. The evaluator runs the same submitted bytes
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

- `P_CONVERT_V_AIN_TO_THE_NEAREST`: Convert `V(ain)` to the nearest integer code using half-up rounding.
- `P_CLAMP_THE_CODE_TO_THE_VALID`: Clamp the code to the valid 5-bit trim range `0..31`.
- `P_DRIVE_DOUT0_DOUT4_FROM_THE_CLAMPED`: Drive `dout0..dout4` from the clamped binary code, LSB first.
- `P_DRIVE_HIGH_BITS_NEAR_VH_AND`: Drive high bits near `vh` and low bits near 0 V.
- `P_UPDATE_DETERMINISTICALLY_AS_THE_ANALOG_INPUT`: Update deterministically as the analog input changes.

The required trace names are: `time`, `ain`, `dout0`, `dout1`, `dout2`, `dout3`, `dout4`.

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
