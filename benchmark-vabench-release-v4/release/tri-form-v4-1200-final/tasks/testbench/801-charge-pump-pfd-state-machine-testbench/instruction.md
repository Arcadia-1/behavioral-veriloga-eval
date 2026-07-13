# Charge Pump PFD State Machine Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Charge Pump PFD State Machine` DUT. The evaluator runs the same submitted bytes
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

- `P_AN_INTEGER_STATE_Q_HELD_IN`: An integer `state_q` held in `[-1, 0, +1]`, initialized to `0`.
- `P_ON_EACH_RISING_CROSSING_OF_V`: On each rising crossing of `V(ref)` through `vth` (`@(cross(V(ref) - vth, +1))`),
- `P_ON_EACH_RISING_CROSSING_OF_V_2`: On each rising crossing of `V(fb)` through `vth` (`@(cross(V(fb) - vth, +1))`),
- `P_MAINTAIN_A_CONTROL_VOLTAGE_VCTRL_Q`: Maintain a control voltage `vctrl_q`, initialized to `vctrl_init`. On a fixed
- `P_DRIVE_VCTRL_TRANSITION_VCTRL_Q_0`: Drive `vctrl = transition(vctrl_q, 0, tedge, tedge)`.
- `P_DRIVE_METRIC_AS_A_VOLTAGE_CODED`: Drive `metric` as a voltage-coded copy of the detector state:

The required trace names are: `time`, `ref`, `fb`, `vctrl`, `metric`.

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
