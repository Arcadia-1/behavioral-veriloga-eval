# Charge Pump PFD State Machine Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `charge_pump_pfd_state_machine.va`: `charge_pump_pfd_state_machine`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_AN_INTEGER_STATE_Q_HELD_IN`: An integer `state_q` held in `[-1, 0, +1]`, initialized to `0`.
- `P_ON_EACH_RISING_CROSSING_OF_V`: On each rising crossing of `V(ref)` through `vth` (`@(cross(V(ref) - vth, +1))`),
- `P_ON_EACH_RISING_CROSSING_OF_V_2`: On each rising crossing of `V(fb)` through `vth` (`@(cross(V(fb) - vth, +1))`),
- `P_MAINTAIN_A_CONTROL_VOLTAGE_VCTRL_Q`: Maintain a control voltage `vctrl_q`, initialized to `vctrl_init`. On a fixed
- `P_DRIVE_VCTRL_TRANSITION_VCTRL_Q_0`: Drive `vctrl = transition(vctrl_q, 0, tedge, tedge)`.
- `P_DRIVE_METRIC_AS_A_VOLTAGE_CODED`: Drive `metric` as a voltage-coded copy of the detector state:

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `charge_pump_pfd_state_machine.va`.
Every supplied `.va` file is editable; do not add or omit files.
