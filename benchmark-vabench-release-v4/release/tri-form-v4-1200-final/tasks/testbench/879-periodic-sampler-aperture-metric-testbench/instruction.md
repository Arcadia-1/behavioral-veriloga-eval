# Periodic Sampler with Aperture Metric Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Periodic Sampler with Aperture Metric` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEARS_THE_HELD_VALUE_APERTURE`: Reset clears the held value, aperture metric, and valid flag.
- `P_ON_EACH_RISING_CLK_EDGE_WITH`: On each rising `clk` edge with `sample_en` high, capture `vin` into `vhold`.
- `P_THE_APERTURE_METRIC_AFTER_A_CAPTURE`: The aperture metric after a capture is proportional to the absolute difference between the new sample and the previous held sample.
- `P_HOLD_VHOLD_AND_THE_LAST_METRIC`: Hold `vhold` and the last metric between enabled sampling events.
- `P_VALID_IS_HIGH_AFTER_THE_FIRST`: `valid` is high after the first enabled sample and low during reset.

The required trace names are: `time`, `vin`, `clk`, `rst`, `sample_en`, `vhold`, `aperture_metric`, `valid`.

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
