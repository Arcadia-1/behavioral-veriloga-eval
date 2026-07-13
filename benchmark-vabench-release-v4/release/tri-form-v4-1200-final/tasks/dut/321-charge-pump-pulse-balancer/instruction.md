# Charge-pump Pulse Balancer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `charge_pump_pulse_balancer.va`: `charge_pump_pulse_balancer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vctrl` to `vcm`, clear imbalance, and clear `balanced`.
- `P_ON_EACH_RISING_CLK_EDGE_OBSERVE`: On each rising `clk` edge, observe voltage-coded `up` and `dn` pulse states.
- `P_INCREASE_VCTRL_FOR_UP_ONLY_DECREASE`: Increase `vctrl` for UP-only, decrease it for DN-only, and hold for simultaneous or inactive pulses.
- `P_DRIVE_IMBALANCE_METRIC_FROM_THE_ACCUMULATED`: Drive `imbalance_metric` from the accumulated UP-minus-DN activity.
- `P_ASSERT_BALANCED_ONLY_WHEN_THE_RECENT`: Assert `balanced` only when the recent absolute imbalance is below `balance_tol`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `charge_pump_pulse_balancer.va`.
Do not add or omit artifacts.
