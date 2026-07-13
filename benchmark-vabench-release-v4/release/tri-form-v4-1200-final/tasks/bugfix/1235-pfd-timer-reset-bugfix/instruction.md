# PFD Timer Reset Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pfd_timer_reset.va`: `pfd_timer_reset`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PFD_STATE_AND_POLARITY`: A rising crossing of `a` asserts the UP state and a rising crossing of `b` asserts the DOWN state; drive `ub` active-low for UP and `d` active-high for DOWN.
- `P_DELAYED_MUTUAL_RESET`: After both detector states have occurred, schedule the mutual reset after `reset_delay` instead of clearing immediately or never clearing.
- `P_OUTPUT_LEVELS_AND_TRANSITIONS`: Drive asserted/deasserted outputs near the public `vh`/`0 V` levels with the declared transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pfd_timer_reset.va`.
Every supplied `.va` file is editable; do not add or omit files.
