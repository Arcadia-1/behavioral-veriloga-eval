# DLL Delay-line Lock

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dll_top.va`: `dll_top`
- `phase_detector.va`: `phase_detector`
- `delay_line.va`: `delay_line`
- `lock_detector.va`: `lock_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation restores delay_center, clears correction and lock outputs, cancels pending edges, and drives delayed_clk low.
- `P_DELAY_LINE_DERIVATION`: Each delayed-clock edge derives from the matching input-clock edge using the code selected for that edge; the output is not free-running.
- `P_PHASE_CORRECTION`: Completed ref/delayed comparisons request the correction direction that moves the delay code toward edge alignment and update the code once within 0 through 31.
- `P_LOCK_QUALIFICATION`: Lock asserts only after four consecutive comparisons within lock_window times unit_delay and clears after an out-of-window comparison.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dll_top.va`, `phase_detector.va`, `delay_line.va`, `lock_detector.va`.
Do not add or omit artifacts.
