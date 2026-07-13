# Slew Rate DAC4 Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Slew Rate DAC4` DUT. The evaluator runs the same submitted bytes
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

- `P_BINARY_MAPPING`: d3 is the MSB and d0 is the LSB of an unsigned four-bit code whose target output is binary weighted.
- `P_ENDPOINTS`: Code 0 targets 0 V and code 15 targets vref.
- `P_CODE_MONOTONICITY`: A larger stable input code does not produce a lower settled output voltage.
- `P_SLEW_LIMIT`: During a target change, the magnitude of the output slope does not exceed slewrate.
- `P_SETTLED_TARGET`: After sufficient time at a stable code, vout reaches the corresponding code-to-vref target.

The required trace names are: `time`, `d3`, `d2`, `d1`, `d0`, `vout`.

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
