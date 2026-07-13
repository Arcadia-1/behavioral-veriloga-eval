# PFD With External Active Low Reset Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PFD With External Active Low Reset` DUT. The evaluator runs the same submitted bytes
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

- `P_WHEN_RSTB_IS_BELOW_VTH_CLEAR`: When `rstb` is below `vth`, clear both PFD states and hold both outputs low. While `rstb` is high, a rising crossing of `ref` asserts `up`, and a rising crossing of `fb` asserts `down`. Once both states have occurred, schedule a reset after `reset_delay` and clear both states at that timer event. The reset input must also clear a pending one-sided UP or DOWN state even if the opposite edge has not arrived.
- `P_VTH_0_45_V_THRESHOLD_FOR`: `vth = 0.45 V`: threshold for `ref`, `fb`, and `rstb`.
- `P_VH_0_9_V_LOGIC_HIGH`: `vh = 0.9 V`: logic-high output level.
- `P_RESET_DELAY_80_PS_FROM_0`: `reset_delay = 80 ps from [0:inf)`: delay from the moment both detector states are asserted to the mutual reset event.
- `P_TR_10_PS_FROM_0_INF`: `tr = 10 ps from [0:inf)`: output transition smoothing time.
- `P_VTH_0_45_V_THRESHOLD_FOR_2`: - `vth = 0.45 V`: threshold for `ref`, `fb`, and `rstb`. - `vh = 0.9 V`: logic-high output level. - `reset_delay = 80 ps from [0:inf)`: delay from the moment both detector states are asserted to the mutual reset event. - `tr = 10 ps from [0:inf)`: output transition smoothing time.

The required trace names are: `time`, `down`, `fb`, `ref`, `rstb`, `up`.

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
