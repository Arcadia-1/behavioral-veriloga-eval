# Start Gated Offset Search Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Start Gated Offset Search` DUT. The evaluator runs the same submitted bytes
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

- `P_DISABLED_COMMON_MODE`: While START is below vstart_th, VINP and VINN both equal vcm and the internal search state is reset.
- `P_START_REINITIALIZATION`: Each rising START crossing through vstart_th reinitializes differential value to zero, step to 20 mV, and remembered direction high.
- `P_FALLING_CLOCK_UPDATES`: While START is high, search updates occur only on falling CLK crossings through vdd/2.
- `P_DECISION_DIRECTED_STEP`: At each enabled update, VOUT above vdd/2 moves the differential value positive and VOUT at or below vdd/2 moves it negative.
- `P_REVERSAL_STEP_HALVING`: When the newly sampled decision direction differs from the remembered direction, the current step is halved before applying the move.
- `P_COMMON_MODE_AND_DIFFERENTIAL`: During search, the average of VINP and VINN remains vcm and their difference equals the accumulated differential search value.

The required trace names are: `time`, `clk`, `vout`, `start`, `vinp`, `vinn`.

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
