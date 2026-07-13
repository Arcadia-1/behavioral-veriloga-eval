# Charge-pump Pulse Balancer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `charge_pump_pulse_balancer.va`: `charge_pump_pulse_balancer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vctrl` to `vcm`, clear imbalance, and clear `balanced`.
- `P_ON_EACH_RISING_CLK_EDGE_OBSERVE`: On each rising `clk` edge, observe voltage-coded `up` and `dn` pulse states.
- `P_INCREASE_VCTRL_FOR_UP_ONLY_DECREASE`: Increase `vctrl` for UP-only, decrease it for DN-only, and hold for simultaneous or inactive pulses.
- `P_DRIVE_IMBALANCE_METRIC_FROM_THE_ACCUMULATED`: Drive `imbalance_metric` from the accumulated UP-minus-DN activity.
- `P_ASSERT_BALANCED_ONLY_WHEN_THE_RECENT`: Assert `balanced` only when the recent absolute imbalance is below `balance_tol`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `charge_pump_pulse_balancer.va`.
Every supplied `.va` file is editable; do not add or omit files.
