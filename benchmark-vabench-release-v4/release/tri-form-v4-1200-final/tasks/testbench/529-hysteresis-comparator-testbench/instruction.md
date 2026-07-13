# Hysteresis Comparator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Hysteresis Comparator` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_DECISION`: OUTP initializes high only when the initial differential exceeds positive vhys over two; otherwise OUTP initializes low and OUTN high.
- `P_POSITIVE_SWITCH_THRESHOLD`: The low OUTP state switches high only on a rising differential crossing of positive vhys over two.
- `P_NEGATIVE_SWITCH_THRESHOLD`: The high OUTP state switches low only on a falling differential crossing of negative vhys over two.
- `P_HYSTERESIS_HOLD`: The previous decision is retained while the differential remains inside the hysteresis band.
- `P_COMPLEMENTARY_RAIL_OUTPUT`: OUTP and OUTN remain complementary and use the local VDD and VSS rail levels after smoothing.

The required trace names are: `time`, `vinp`, `vinn`, `out_p`, `out_n`, `vss`, `vdd`.

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
