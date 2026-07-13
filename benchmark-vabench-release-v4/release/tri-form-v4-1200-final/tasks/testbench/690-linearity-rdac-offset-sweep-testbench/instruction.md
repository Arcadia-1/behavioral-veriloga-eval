# Linearity RDAC Offset Sweep Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Linearity RDAC Offset Sweep` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_SWEEP_DIRECTION`: Rising `ck` crossings implement the RDAC sweep using `d < 0.5*vdd` as the low comparator direction.
- `P_SWEEP_INITIAL_STATE`: Initialize `vref`, `vin`, search step, and stored comparator direction to the declared sweep state.
- `P_ITERATIVE_SEARCH_UPDATES`: For each RDAC code, run exactly `iter_num` search-update clocks and halve the step before moving on direction changes.
- `P_CODE_UPDATE_AND_RECENTER`: The clock after each search window updates the 7-bit code, recenters the search, and advances the sweep without an extra search step.

The required trace names are: `time`, `ck`, `d`, `dc0`, `dc1`, `dc2`, `dc3`, `dc4`, `dc5`, `dc6`, `vinn`, `vinp`, `vrefn`, `vrefp`.

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
