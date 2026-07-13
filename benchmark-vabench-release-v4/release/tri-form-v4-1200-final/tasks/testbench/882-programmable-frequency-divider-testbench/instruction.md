# Programmable Frequency Divider Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Programmable Frequency Divider` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_OR_LOW_ENABLE_CLEARS_THE`: Reset or low `enable` clears the divider state, `clk_div`, `ratio_metric`, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_IN`: On each enabled rising `clk_in` edge, sample the four control bits and form divisor `N = code + 1`.
- `P_TOGGLE_CLK_DIV_WHENEVER_N_ENABLED`: Toggle `clk_div` whenever `N` enabled input-clock rising edges have been counted.
- `P_RATIO_METRIC_EXPOSES_THE_SAMPLED_DIVISOR`: `ratio_metric` exposes the sampled divisor as a voltage-coded fraction of the 1-to-16 range.
- `P_VALID_IS_HIGH_AFTER_THE_FIRST`: `valid` is high after the first divider toggle and low before that or during reset/disable.

The required trace names are: `time`, `clk_in`, `rst`, `enable`, `n_3`, `n_2`, `n_1`, `n_0`, `clk_div`, `ratio_metric`, `valid`.

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
