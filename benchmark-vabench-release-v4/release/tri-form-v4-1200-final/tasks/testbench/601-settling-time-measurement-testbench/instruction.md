# Settling Time Measurement Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Settling Time Measurement` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_ZERO_STATE`: The settling-response state initializes to 0 V and vout begins from that state.
- `P_FIRST_ORDER_UPDATE`: At each 1 ns update, the response advances by 0.04 times the difference between step and its previous value.
- `P_RESPONSE_CONVERGENCE`: For a constant input step, vout approaches the step value monotonically without overshoot under the public recurrence.
- `P_DONE_TIME_GATE`: Done remains low through 120 ns regardless of the response level.
- `P_DONE_SETTLED_GATE`: After 120 ns, done is high only while the internal settled response is above 0.75 V and otherwise remains low.

The required trace names are: `time`, `step`, `vout`, `done`.

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
