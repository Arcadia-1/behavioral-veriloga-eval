# Frequency-word DCO with Divider Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Frequency-word DCO with Divider Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_STOP`: Reset or disabled operation stops and clears both clocks, the divider counter, and the frequency metric.
- `P_FREQUENCY_WORD_MAPPING`: The six-bit frequency word maps to min(f_max, f_min plus f_step times code), with the public normalized metric matching that target.
- `P_DIVIDER_MONITOR`: div_clk toggles once per divide_ratio rising DCO edges and its counter restarts after reset or disable.
- `P_RESTART_MONOTONICITY`: Enable restarts both clocks low with the first DCO rise one half-period later, and larger frequency words produce nondecreasing edge counts.

The required trace names are: `time`, `enable`, `rst`, `fcw_5`, `fcw_4`, `fcw_3`, `fcw_2`, `fcw_1`, `fcw_0`, `dco_clk`, `div_clk`, `freq_metric`.

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
