# BBPD Data Edge Alignment Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `BBPD Data Edge Alignment` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_RETIMING`: Each rising clk edge captures the current data logic level onto retimed_data, which holds between clock edges.
- `P_EARLY_TRANSITION_UP`: A data transition closer to the upcoming nominal clock edge and outside the deadzone produces an UP pulse of pulse_w duration.
- `P_LATE_TRANSITION_DN`: A data transition closer to the previous nominal clock edge and outside the deadzone produces a DN pulse of pulse_w duration.
- `P_DEADZONE_SUPPRESSION`: Data transitions within deadzone of the relevant nominal clock edge produce neither correction pulse.
- `P_BOTH_DATA_POLARITIES`: Both rising and falling data transitions participate in timing classification.
- `P_MUTUAL_EXCLUSION`: UP and DN are mutually exclusive apart from finite analog transition overlap and use the vdd-to-vss logic range.

The required trace names are: `time`, `vdd`, `vss`, `clk`, `data`, `up`, `dn`, `retimed_data`.

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
