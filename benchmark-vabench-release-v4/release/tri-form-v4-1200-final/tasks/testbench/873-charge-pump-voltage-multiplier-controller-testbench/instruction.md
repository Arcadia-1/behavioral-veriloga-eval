# Charge-pump Voltage Multiplier Controller Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Charge-pump Voltage Multiplier Controller` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset clears vout, pump control, readiness, and regulation state; disabled operation suppresses pumping.
- `P_NONOVERLAP_PHASES`: Enabled clock updates alternate phase_a and phase_b while never asserting both phases together.
- `P_PUMP_REGULATION`: While pump_en is active, enabled phase updates raise vout in bounded pump steps; without pumping, vout leaks downward and remains within rails.
- `P_ERROR_REPORTING`: regulation_error continuously reports target minus vout and pump_en requests pumping below the lower tolerance boundary.
- `P_READY_QUALIFICATION`: Ready asserts only after three consecutive enabled clock updates within the regulation tolerance and clears outside qualification.

The required trace names are: `time`, `clk`, `rst`, `enable`, `target`, `vout`, `phase_a`, `phase_b`, `pump_en`, `regulation_error`, `ready`.

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
