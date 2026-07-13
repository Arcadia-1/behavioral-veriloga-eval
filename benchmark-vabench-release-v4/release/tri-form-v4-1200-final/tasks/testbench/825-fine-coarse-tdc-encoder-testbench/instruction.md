# Fine/coarse TDC Encoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Fine/coarse TDC Encoder` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear coarse code, fine metric, and `valid`.
- `P_A_RISING_START_EDGE_ARMS_A`: A rising `start` edge arms a measurement and clears the coarse counter.
- `P_COUNT_RISING_REF_CLK_EDGES_UNTIL`: Count rising `ref_clk` edges until the first rising `stop` edge.
- `P_LATCH_THE_COARSE_COUNT_INTO_COARSE`: Latch the coarse count into `coarse_3..coarse_0` and expose a fine residual proxy on `fine_metric`.
- `P_ASSERT_VALID_ONLY_AFTER_THE_STOP`: Assert `valid` only after the stop edge completes the measurement.

The required trace names are: `time`, `start`, `stop`, `ref_clk`, `rst`, `enable`, `coarse_3`, `coarse_2`, `coarse_1`, `coarse_0`, `fine_metric`, `valid`.

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
