# Sine Periodic Voltage Source Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sine Periodic Voltage Source` DUT. The evaluator runs the same submitted bytes
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

- `P_FIRST_TONE`: The output includes a zero-phase sine component with frequency f1 and signed amplitude a1.
- `P_SECOND_TONE`: The output includes a zero-phase sine component with frequency f2 and signed amplitude a2.
- `P_THIRD_TONE`: The output includes a zero-phase sine component with frequency f3 and signed amplitude a3.
- `P_LINEAR_SUPERPOSITION`: At every transient time t, OUT equals a1*sin(2*pi*f1*t) plus a2*sin(2*pi*f2*t) plus a3*sin(2*pi*f3*t).
- `P_ZERO_INITIAL_PHASE`: With no added offset and zero initial phase for all tones, OUT is 0 V at t = 0.

The required trace names are: `time`, `OUT`.

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
