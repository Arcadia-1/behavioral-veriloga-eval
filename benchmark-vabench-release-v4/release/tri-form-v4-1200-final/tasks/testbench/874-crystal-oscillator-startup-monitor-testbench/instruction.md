# Crystal Oscillator Startup Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Crystal Oscillator Startup Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, clear oscillator amplitude, `osc_out`, `valid`, and `startup_done`.
- `P_INCREASE_A_BEHAVIORAL_AMPLITUDE_STATE_BY`: Increase a behavioral amplitude state by `amp_step` on each rising `clk_ref` edge while enabled until `amp_target` is reached.
- `P_CLAMP_THE_AMPLITUDE_AT_AMP_TARGET`: Clamp the amplitude at `amp_target` and expose it on `amp_metric`.
- `P_TOGGLE_OSC_OUT_FROM_CLK_REF`: Toggle `osc_out` from `clk_ref` only after the amplitude state is nonzero.
- `P_ASSERT_STARTUP_DONE_WHEN_AMP_METRIC`: Assert `startup_done` when `amp_metric` reaches `amp_target`.
- `P_ASSERT_VALID_AFTER_TWO_CONSECUTIVE_SLICED`: Assert `valid` after two consecutive sliced oscillator periods after startup is done.

The required trace names are: `time`, `enable`, `rst`, `clk_ref`, `osc_out`, `amp_metric`, `valid`, `startup_done`.

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
