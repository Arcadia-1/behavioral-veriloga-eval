# DLL Delay-line Lock Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DLL Delay-line Lock` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation restores delay_center, clears correction and lock outputs, cancels pending edges, and drives delayed_clk low.
- `P_DELAY_LINE_DERIVATION`: Each delayed-clock edge derives from the matching input-clock edge using the code selected for that edge; the output is not free-running.
- `P_PHASE_CORRECTION`: Completed ref/delayed comparisons request the correction direction that moves the delay code toward edge alignment and update the code once within 0 through 31.
- `P_LOCK_QUALIFICATION`: Lock asserts only after four consecutive comparisons within lock_window times unit_delay and clears after an out-of-window comparison.

The required trace names are: `time`, `ref_clk`, `in_clk`, `rst`, `enable`, `delayed_clk`, `up`, `down`, `delay_4`, `delay_3`, `delay_2`, `delay_1`, `delay_0`, `lock`.

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
