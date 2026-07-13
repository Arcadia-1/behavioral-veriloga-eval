# PFD Timer Reset

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pfd_timer_reset.va`: `pfd_timer_reset`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PFD_STATE_AND_POLARITY`: A rising crossing of `a` asserts the UP state and a rising crossing of `b` asserts the DOWN state; drive `ub` active-low for UP and `d` active-high for DOWN.
- `P_DELAYED_MUTUAL_RESET`: After both detector states have occurred, schedule the mutual reset after `reset_delay` instead of clearing immediately or never clearing.
- `P_OUTPUT_LEVELS_AND_TRANSITIONS`: Drive asserted/deasserted outputs near the public `vh`/`0 V` levels with the declared transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pfd_timer_reset.va`.
Do not add or omit artifacts.
