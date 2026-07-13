# Config Latch 32b Clocked Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Config Latch 32b Clocked` DUT. The evaluator runs the same submitted bytes
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

- `P_ENABLED_PASS`: When en is high, every q bit equals the corresponding voltage-coded d bit.
- `P_DISABLED_CLEAR`: When en is low, every q bit is driven low regardless of the data input.
- `P_STATIC_ENABLE_BEHAVIOR`: The public interface is combinational enable gating: q follows data changes while enabled and does not retain a prior word while disabled.
- `P_BIT_ALIGNMENT`: Each d[N] controls only the same-index q[N]; bus order is not reversed or shifted.
- `P_OUTPUT_LEVELS`: Each q bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

The required trace names are: `time`, `en`, `d31`, `d30`, `d29`, `d28`, `d27`, `d26`, `d25`, `d24`, `d23`, `d22`, `d21`, `d20`, `d19`, `d18`, `d17`, `d16`, `d15`, `d14`, `d13`, `d12`, `d11`, `d10`, `d9`, `d8`, `d7`, `d6`, `d5`, `d4`, `d3`, `d2`, `d1`, `d0`, `q31`, `q30`, `q29`, `q28`, `q27`, `q26`, `q25`, `q24`, `q23`, `q22`, `q21`, `q20`, `q19`, `q18`, `q17`, `q16`, `q15`, `q14`, `q13`, `q12`, `q11`, `q10`, `q9`, `q8`, `q7`, `q6`, `q5`, `q4`, `q3`, `q2`, `q1`, `q0`.

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
