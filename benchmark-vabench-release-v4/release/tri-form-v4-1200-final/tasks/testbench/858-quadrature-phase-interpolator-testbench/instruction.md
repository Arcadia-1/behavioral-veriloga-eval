# Quadrature Phase Interpolator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Quadrature Phase Interpolator` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_CLEAR_CLK_OUT_QUADRANT`: On reset, clear `clk_out`, quadrant outputs, and `phase_metric`.
- `P_OBSERVE_THE_RISING_EDGES_OF_CLK`: Observe the rising edges of `clk_i` and `clk_q` and maintain a four-quadrant phase reference.
- `P_DECODE_CODE_4_CODE_0_AS`: Decode `code_4..code_0` as an unsigned phase code from 0 to 31.
- `P_GENERATE_CLK_OUT_EDGES_DELAYED_FROM`: Generate `clk_out` edges delayed from the selected quadrant reference by `unit_delay` times the intra-quadrant code.
- `P_QUADRANT_1_QUADRANT_0_MUST_EXPOSE`: `quadrant_1..quadrant_0` must expose the selected quadrant.
- `P_PHASE_METRIC_MUST_EXPOSE_THE_DECODED`: `phase_metric` must expose the decoded phase code as a voltage-level metric.

The required trace names are: `time`, `clk_i`, `clk_q`, `rst`, `code_4`, `code_3`, `code_2`, `code_1`, `code_0`, `clk_out`, `quadrant_1`, `quadrant_0`, `phase_metric`.

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
