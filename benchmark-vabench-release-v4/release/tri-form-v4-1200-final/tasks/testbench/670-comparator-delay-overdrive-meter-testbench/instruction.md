# Comparator Delay Overdrive Meter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Comparator Delay Overdrive Meter` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCK_ARMED_MEASUREMENT`: Each rising `clk` threshold crossing stores the launch time, captures absolute differential overdrive, and arms exactly one pending measurement.
- `P_DECISION_DELAY_CAPTURE`: The first qualifying `outp` or `outn` decision edge while armed reports the elapsed clock-to-decision delay in `delay_ps`.
- `P_ABSOLUTE_OVERDRIVE_METRIC`: `overdrive_mv` reports the absolute input differential magnitude at launch time.
- `P_POLARITY_AND_VALID_FLAG`: `polarity` reports the winning output decision direction and `valid` asserts only for a completed armed measurement.

The required trace names are: `time`, `clk`, `vinp`, `vinn`, `outp`, `outn`, `delay_ps`, `overdrive_mv`, `polarity`, `valid`.

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
