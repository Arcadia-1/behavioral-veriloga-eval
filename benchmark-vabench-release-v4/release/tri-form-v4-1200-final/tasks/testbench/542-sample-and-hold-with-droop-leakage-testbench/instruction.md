# Sample And Hold With Droop Leakage Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sample And Hold With Droop Leakage` DUT. The evaluator runs the same submitted bytes
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

- `P_SAMPLE_CAPTURE`: Each rising sample crossing while reset is inactive captures the instantaneous vin voltage into the held state.
- `P_HOLD_BETWEEN_EVENTS`: Between sample and leakage events, vout reflects the retained held state rather than continuously tracking vin.
- `P_PERIODIC_DROOP`: At every leak_period update while reset is inactive, the held value is multiplied by decay.
- `P_RESET_CLEAR`: Active reset clears the held state to 0 V at sampling or leakage update events.
- `P_SMOOTH_OUTPUT`: Vout approaches each held-state target with the finite transition smoothing set by tr.

The required trace names are: `time`, `sample`, `rst`, `vin`, `vout`.

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
