# Offset-calibrated Comparator System Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Offset-calibrated Comparator System` DUT. The evaluator runs the same submitted bytes
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

- `P_CAL_RESET_CLEAR`: Reset clears offset code, decision, ready, and threshold_dbg.
- `P_CAL_CODE_UPDATE`: Each enabled rising clock updates and clamps the offset code in the direction selected by cal_ref.
- `P_CAL_OFFSET_DAC`: threshold_dbg equals signed code minus eight times offset_lsb outside reset.
- `P_CAL_READY_QUALIFICATION`: ready asserts after four updates in one calibration window and the code holds while cal_en is low.
- `P_CAL_COMPARATOR_DECISION`: decision reflects the sign of vinp minus vinn plus threshold_dbg and is low in reset.

The required trace names are: `time`, `vinp`, `vinn`, `clk`, `rst`, `cal_en`, `cal_ref`, `decision`, `ready`, `offset_3`, `offset_2`, `offset_1`, `offset_0`, `threshold_dbg`.

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
