# PLL Timing Monitor System Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pll_timing_monitor_top.va`: `pll_timing_monitor_top`
- `phase_detector.va`: `phase_detector`
- `divider.va`: `divider`
- `lock_detector.va`: `lock_detector`
- `reacquire_timer.va`: `reacquire_timer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable clears pulse, lock, reacquire, divider, and phase-code outputs.
- `P_PHASE_COMPARE`: UP and DOWN identify which observed rising edge led each completed comparison.
- `P_PHASE_CODE`: The offset-binary phase code updates by one per completed comparison and clamps to its public range.
- `P_DIVIDE_BY_FOUR_EDGES`: DIV2 toggles after each pair of feedback-clock rising edges.
- `P_LOCK_REACQUIRE`: Lock requires four consecutive in-window comparisons and reacquire requires two post-lock out-of-window comparisons.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pll_timing_monitor_top.va`, `phase_detector.va`, `divider.va`, `lock_detector.va`, `reacquire_timer.va`.
Every supplied `.va` file is editable; do not add or omit files.
