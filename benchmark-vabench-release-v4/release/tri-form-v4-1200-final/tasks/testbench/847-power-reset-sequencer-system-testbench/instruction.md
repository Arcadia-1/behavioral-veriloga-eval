# Power and Reset Sequencer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Power and Reset Sequencer` DUT. The evaluator runs the same submitted bytes
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

- `P_PWR_ASYNC_CLEAR`: External reset or a brownout clears por_n, core reset release, enables, and ready without waiting for sequence completion.
- `P_PWR_POR_DEBOUNCE`: por_n asserts only after two consecutive good-power rising clock edges.
- `P_PWR_SEQUENCE_ORDER`: With power good and enable requested, rst_n_core, en_ana, and en_dig release on successive rising clock edges.
- `P_PWR_READY_DELAY`: ready asserts one rising clock after both enables are high.

The required trace names are: `time`, `vdd_sense`, `clk`, `rst_n_ext`, `enable_req`, `por_n`, `rst_n_core`, `en_ana`, `en_dig`, `ready`.

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
