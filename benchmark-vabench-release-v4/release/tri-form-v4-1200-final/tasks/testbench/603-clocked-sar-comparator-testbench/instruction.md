# Clocked SAR Comparator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked SAR Comparator` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_PRECHARGE`: Both decision outputs initialize high at vdd.
- `P_FALLING_EDGE_PRECHARGE`: Each falling CMPCK crossing through vdd/2 resets both DCMPN and DCMPP high.
- `P_POSITIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP greater than VINN, DCMPP is high and DCMPN is low.
- `P_NEGATIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP less than VINN, DCMPN is high and DCMPP is low.
- `P_EQUAL_INPUT_DECISION`: On a rising CMPCK crossing with equal differential inputs, both decision outputs become low.
- `P_LATCHED_HOLD_AND_TIMING`: The precharged or decided state holds between clock events and output changes use td_cmp delay and tr smoothing.

The required trace names are: `time`, `cmpck`, `vinn`, `vinp`, `dcmpn`, `dcmpp`.

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
