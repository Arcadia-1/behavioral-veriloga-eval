# VCO Phase Integrator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `VCO Phase Integrator` DUT. The evaluator runs the same submitted bytes
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

- `P_PERIODIC_PHASE_UPDATE`: Phase state updates on the public 1 ns periodic schedule by 0.03 plus 0.09 times vctrl.
- `P_WRAPPED_PHASE_RANGE`: The observable phase remains in the normalized range from 0 inclusive to 1 exclusive.
- `P_WRAP_TOGGLES_CLOCK`: Each phase wrap by one cycle toggles the voltage-coded clock between 0 V and 0.9 V.
- `P_CONTROLLED_EDGE_RATE`: A sustained higher vctrl produces more clock toggles over the same observation interval than a sustained lower vctrl.

The required trace names are: `time`, `vctrl`, `phase`, `clk`.

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
