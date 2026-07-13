# Bidirectional Hybrid Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bidirectional Hybrid Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEAR`: Reset centers the continuous sum and difference outputs and clears sampled metrics and balance qualification.
- `P_SUM_DIFF_MAPPING`: sum_out and diff_out implement the clipped common and differential mappings of port_a and port_b around vcm.
- `P_TRIM_RESPONSE`: The signed three-bit trim correction shifts sum and difference in opposite directions by trim_lsb per code.
- `P_DIRECTIONAL_METRICS`: At rising clock edges forward and reverse metrics reconstruct the directional components from the mapped sum and difference outputs.
- `P_BALANCE_QUALIFICATION`: balance_ok asserts only after two consecutive metric updates whose directional mismatch is within balance_tol.

The required trace names are: `time`, `port_a`, `port_b`, `clk`, `rst`, `trim_2`, `trim_1`, `trim_0`, `sum_out`, `diff_out`, `forward_metric`, `reverse_metric`, `balance_ok`.

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
