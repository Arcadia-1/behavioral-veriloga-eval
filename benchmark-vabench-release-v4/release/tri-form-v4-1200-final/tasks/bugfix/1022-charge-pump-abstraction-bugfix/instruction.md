# Charge Pump Abstraction Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `charge_pump_abstraction.va`: `charge_pump_abstraction`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_MIDSCALE`: When rst is high, vctrl resets to the midpoint of vmin and vmax and metric is 0.45 V.
- `P_UP_ONLY_STEP`: A rising clock crossing sampling up high and dn low increases vctrl by step and encodes metric at 0.75 V.
- `P_DN_ONLY_STEP`: A rising clock crossing sampling dn high and up low decreases vctrl by step and encodes metric at 0.15 V.
- `P_HOLD_CASES`: A rising clock crossing sampling both or neither request holds vctrl and encodes metric at 0.45 V.
- `P_CONTROL_CLAMP`: Repeated sampled movement cannot drive vctrl below vmin or above vmax.
- `P_SAMPLED_HOLD`: Changes on up or dn between rising clock crossings do not immediately change vctrl.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `charge_pump_abstraction.va`.
Every supplied `.va` file is editable; do not add or omit files.
