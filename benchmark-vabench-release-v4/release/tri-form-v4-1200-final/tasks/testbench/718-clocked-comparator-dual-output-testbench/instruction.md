# Clocked Comparator Dual Output Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked Comparator Dual Output` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIALIZE_BOTH_DECISION_OUTPUTS_LOW`: Initialize both decision outputs low.
- `P_WHENEVER_CLK_FALLS_THROUGH_VDD_2`: Whenever `clk` falls through `vdd/2`, reset both outputs low.
- `P_WHENEVER_CLK_RISES_THROUGH_VDD_2`: Whenever `clk` rises through `vdd/2`, latch a differential decision.
- `P_DRIVE_OUTP_HIGH_AND_OUTN_LOW`: Drive `outp` high and `outn` low for `vinp > vinn`.
- `P_DRIVE_OUTN_HIGH_AND_OUTP_LOW`: Drive `outn` high and `outp` low for `vinp < vinn`.
- `P_DRIVE_BOTH_OUTPUTS_LOW_FOR_AN`: Drive both outputs low for an equal-input decision.

The required trace names are: `time`, `clk`, `vinn`, `vinp`, `outn`, `outp`.

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
