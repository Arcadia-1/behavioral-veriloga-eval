# CTLE Equalizer Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `CTLE Equalizer Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_INITIALIZES_THE_EQUALIZED_OUTPUT_TO`: Reset initializes the equalized output to common mode and clears metric outputs.
- `P_ON_EACH_RISING_CLK_SAMPLE_THE`: On each rising `clk`, sample the boost code and the current input.
- `P_DRIVE_VOUT_FROM_THE_CURRENT_INPUT`: Drive `vout` from the current input plus a boost-code-scaled edge term relative to the previous sampled input.
- `P_CLAMP_VOUT_TO_THE_VSS_TO`: Clamp `vout` to the `vss` to `vdd` range.
- `P_EDGE_METRIC_REPORTS_THE_ABSOLUTE_BOOSTED`: `edge_metric` reports the absolute boosted edge contribution after clipping to full scale.
- `P_SAT_FLAG_IS_HIGH_WHEN_THE`: `sat_flag` is high when the unclamped equalized target would exceed either output rail.

The required trace names are: `time`, `vin`, `clk`, `rst`, `boost_2`, `boost_1`, `boost_0`, `vout`, `edge_metric`, `sat_flag`.

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
