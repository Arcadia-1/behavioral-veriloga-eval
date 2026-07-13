# Deserializer DEMUX Alignment Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Deserializer DEMUX Alignment Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear all parallel outputs, `phase_metric`, and `word_valid`.
- `P_A_RISING_ALIGN_PULSE_RESETS_THE`: A rising `align_pulse` resets the slot pointer so the next sampled serial bit is written to `out0`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample `serial_in` into the active output slot and advance the slot pointer.
- `P_ASSERT_WORD_VALID_AFTER_ALL_FOUR`: Assert `word_valid` after all four output slots have been updated since the most recent alignment event.
- `P_PHASE_METRIC_MUST_EXPOSE_THE_ACTIVE`: `phase_metric` must expose the active slot pointer.

The required trace names are: `time`, `clk`, `rst`, `enable`, `serial_in`, `align_pulse`, `out0`, `out1`, `out2`, `out3`, `phase_metric`, `word_valid`.

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
