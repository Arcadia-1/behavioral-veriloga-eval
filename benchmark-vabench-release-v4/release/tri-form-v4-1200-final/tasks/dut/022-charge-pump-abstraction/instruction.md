# Charge Pump Abstraction

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `charge_pump_abstraction.va`: `charge_pump_abstraction`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_MIDSCALE`: When rst is high, vctrl resets to the midpoint of vmin and vmax and metric is 0.45 V.
- `P_UP_ONLY_STEP`: A rising clock crossing sampling up high and dn low increases vctrl by step and encodes metric at 0.75 V.
- `P_DN_ONLY_STEP`: A rising clock crossing sampling dn high and up low decreases vctrl by step and encodes metric at 0.15 V.
- `P_HOLD_CASES`: A rising clock crossing sampling both or neither request holds vctrl and encodes metric at 0.45 V.
- `P_CONTROL_CLAMP`: Repeated sampled movement cannot drive vctrl below vmin or above vmax.
- `P_SAMPLED_HOLD`: Changes on up or dn between rising clock crossings do not immediately change vctrl.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `charge_pump_abstraction.va`.
Do not add or omit artifacts.
