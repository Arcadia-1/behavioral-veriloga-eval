# PA AM/PM Memory Tap Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PA AM/PM Memory Tap Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metrics, and clear `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample input amplitude and drive level.
- `P_APPLY_AN_AM_GAIN_COMPRESSION_PROXY`: Apply an AM gain compression proxy as drive increases.
- `P_APPLY_A_ONE_SAMPLE_MEMORY_TERM`: Apply a one-sample memory term that changes output polarity metric after large input changes.
- `P_EXPOSE_AM_AND_PM_PROXIES_SEPARATELY`: Expose AM and PM proxies separately and assert `valid` after the first update.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `drive`, `vout`, `am_metric`, `pm_metric`, `valid`.

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
