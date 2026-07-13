# Edge Interval TDC 8b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Edge Interval TDC 8b` DUT. The evaluator runs the same submitted bytes
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

- `P_START_ARMS`: Each rising start crossing begins a new interval measurement, records that edge time, and clears valid.
- `P_NEXT_STOP_COMPLETES`: The first rising stop crossing after an armed start completes that measurement; stop crossings while unarmed do not change the result.
- `P_INTERVAL_QUANTIZATION`: A completed interval is rounded to the nearest whole nanosecond and reported as an unsigned code.
- `P_CODE_SATURATION`: Measured interval codes are saturated to the inclusive 8-bit range 0 through 255.
- `P_VALID_AND_BIT_ORDER`: valid asserts after completion; code0 is the least significant bit and code7 is the most significant bit, using 0 V and vdd logic levels.

The required trace names are: `time`, `start`, `stop`, `valid`, `code0`, `code1`, `code2`, `code3`, `code4`, `code5`, `code6`, `code7`.

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
