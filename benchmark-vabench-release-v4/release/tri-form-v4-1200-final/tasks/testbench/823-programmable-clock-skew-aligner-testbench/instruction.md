# Programmable Clock Skew Aligner Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Programmable Clock Skew Aligner` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive output and metrics low.
- `P_DECODE_SKEW_2_SKEW_0_AS`: Decode `skew_2..skew_0` as a programmable output-edge delay code.
- `P_FOR_EACH_ACCEPTED_INPUT_CLOCK_EDGE`: For each accepted input clock edge, schedule one output edge after the code-dependent delay.
- `P_EXPOSE_THE_ACTIVE_DELAY_CODE_AS`: Expose the active delay code as `delay_metric`.
- `P_ASSERT_VALID_AFTER_THE_FIRST_DELAYED`: Assert `valid` after the first delayed output edge has been generated.

The required trace names are: `time`, `clk_in`, `rst`, `enable`, `skew_2`, `skew_1`, `skew_0`, `clk_out`, `delay_metric`, `valid`.

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
