# Correlated Double Sampler Offset-cancel Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Correlated Double Sampler Offset-cancel Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_CLEAR_RESET_SAMPLE_SIGNAL`: On reset, clear reset-sample, signal-sample, output, debug metric, and `valid`.
- `P_ON_A_RISING_CLK_EDGE_WITH`: On a rising `clk` edge with `sample_reset` high, capture `vin` as the reset/reference sample.
- `P_ON_A_LATER_RISING_CLK_EDGE`: On a later rising `clk` edge with `sample_signal` high, capture `vin` as the signal sample.
- `P_DRIVE_VOUT_AS_VCM_PLUS_THE`: Drive `vout` as `vcm` plus the signal-minus-reset difference scaled by `cds_gain`.
- `P_EXPOSE_THE_RESET_SAMPLE_ON_OFFSET`: Expose the reset sample on `offset_dbg` and assert `valid` only after a complete reset/signal pair.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin`, `clk`, `rst`, `sample_reset`, `sample_signal`, `vout`, `offset_dbg`, `valid`.

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
