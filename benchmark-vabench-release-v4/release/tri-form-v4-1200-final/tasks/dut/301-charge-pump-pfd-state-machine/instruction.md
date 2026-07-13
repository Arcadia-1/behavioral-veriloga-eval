# Charge Pump PFD State Machine

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `charge_pump_pfd_state_machine.va`: `charge_pump_pfd_state_machine`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_AN_INTEGER_STATE_Q_HELD_IN`: An integer `state_q` held in `[-1, 0, +1]`, initialized to `0`.
- `P_ON_EACH_RISING_CROSSING_OF_V`: On each rising crossing of `V(ref)` through `vth` (`@(cross(V(ref) - vth, +1))`),
- `P_ON_EACH_RISING_CROSSING_OF_V_2`: On each rising crossing of `V(fb)` through `vth` (`@(cross(V(fb) - vth, +1))`),
- `P_MAINTAIN_A_CONTROL_VOLTAGE_VCTRL_Q`: Maintain a control voltage `vctrl_q`, initialized to `vctrl_init`. On a fixed
- `P_DRIVE_VCTRL_TRANSITION_VCTRL_Q_0`: Drive `vctrl = transition(vctrl_q, 0, tedge, tedge)`.
- `P_DRIVE_METRIC_AS_A_VOLTAGE_CODED`: Drive `metric` as a voltage-coded copy of the detector state:

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `charge_pump_pfd_state_machine.va`.
Do not add or omit artifacts.
