# PFD With External Active Low Reset

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pfd_active_low_reset.va`: `pfd_active_low_reset`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_WHEN_RSTB_IS_BELOW_VTH_CLEAR`: When `rstb` is below `vth`, clear both PFD states and hold both outputs low. While `rstb` is high, a rising crossing of `ref` asserts `up`, and a rising crossing of `fb` asserts `down`. Once both states have occurred, schedule a reset after `reset_delay` and clear both states at that timer event. The reset input must also clear a pending one-sided UP or DOWN state even if the opposite edge has not arrived.
- `P_VTH_0_45_V_THRESHOLD_FOR`: `vth = 0.45 V`: threshold for `ref`, `fb`, and `rstb`.
- `P_VH_0_9_V_LOGIC_HIGH`: `vh = 0.9 V`: logic-high output level.
- `P_RESET_DELAY_80_PS_FROM_0`: `reset_delay = 80 ps from [0:inf)`: delay from the moment both detector states are asserted to the mutual reset event.
- `P_TR_10_PS_FROM_0_INF`: `tr = 10 ps from [0:inf)`: output transition smoothing time.
- `P_VTH_0_45_V_THRESHOLD_FOR_2`: - `vth = 0.45 V`: threshold for `ref`, `fb`, and `rstb`. - `vh = 0.9 V`: logic-high output level. - `reset_delay = 80 ps from [0:inf)`: delay from the moment both detector states are asserted to the mutual reset event. - `tr = 10 ps from [0:inf)`: output transition smoothing time.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pfd_active_low_reset.va`.
Do not add or omit artifacts.
