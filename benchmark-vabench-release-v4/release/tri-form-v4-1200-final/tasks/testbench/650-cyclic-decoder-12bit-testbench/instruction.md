# Cyclic Decoder 12bit Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Cyclic Decoder 12bit` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_EDGE_12BIT_DECODE`: Each rising `clks` crossing samples the twelve voltage-coded bits into an unsigned code.
- `P_BIT_WEIGHT_ORDER`: `d0` is the LSB and `d11` is the MSB in the decoded code.
- `P_CENTERED_OUTPUT_SCALE`: The decoded value is normalized to the full 12-bit range, shifted by the half-scale midpoint, and held on `dout`.

The required trace names are: `time`, `clks`, `d0`, `d1`, `d10`, `d11`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`, `dout`.

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
