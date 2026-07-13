# PLL Timing Monitor System

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pll_timing_monitor_top.va`: `pll_timing_monitor_top`
- `phase_detector.va`: `phase_detector`
- `divider.va`: `divider`
- `lock_detector.va`: `lock_detector`
- `reacquire_timer.va`: `reacquire_timer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable clears pulse, lock, reacquire, divider, and phase-code outputs.
- `P_PHASE_COMPARE`: UP and DOWN identify which observed rising edge led each completed comparison.
- `P_PHASE_CODE`: The offset-binary phase code updates by one per completed comparison and clamps to its public range.
- `P_DIVIDE_BY_FOUR_EDGES`: DIV2 toggles after each pair of feedback-clock rising edges.
- `P_LOCK_REACQUIRE`: Lock requires four consecutive in-window comparisons and reacquire requires two post-lock out-of-window comparisons.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pll_timing_monitor_top.va`, `phase_detector.va`, `divider.va`, `lock_detector.va`, `reacquire_timer.va`.
Do not add or omit artifacts.
