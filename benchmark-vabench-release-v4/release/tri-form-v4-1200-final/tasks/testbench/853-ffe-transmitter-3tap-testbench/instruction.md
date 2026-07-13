# 3-tap FFE Transmitter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `3-tap FFE Transmitter` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEARS_SYMBOL_HISTORY_AND_DRIVES`: Reset clears symbol history and drives all outputs to common mode.
- `P_ON_EACH_RISING_CLK_SAMPLE_DATA`: On each rising `clk`, sample `data` as +1 for high and -1 for low.
- `P_DRIVE_MAIN_DBG_PRE_DBG_AND`: Drive `main_dbg`, `pre_dbg`, and `post_dbg` as voltage-coded per-tap contributions around common mode.
- `P_VOUT_IS_THE_CLIPPED_SUM_OF`: `vout` is the clipped sum of the current main contribution, previous-symbol pre contribution, and older-symbol post contribution.
- `P_HIGHER_TAP_CONTROL_CODES_MUST_INCREASE`: Higher tap-control codes must increase the corresponding contribution magnitude.

The required trace names are: `time`, `data`, `clk`, `rst`, `pre_1`, `pre_0`, `post_1`, `post_0`, `vout`, `main_dbg`, `pre_dbg`, `post_dbg`.

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
