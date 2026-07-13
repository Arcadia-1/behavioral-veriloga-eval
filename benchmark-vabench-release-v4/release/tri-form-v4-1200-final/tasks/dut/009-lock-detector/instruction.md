# Lock Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `lock_detector.va`: `lock_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ALIGNMENT_STREAK`: lock asserts only after need consecutive reference edges whose most recent feedback edge is within tol.
- `P_PREMATURE_LOCK`: lock remains low before the need-th consecutive aligned reference event.
- `P_MISS_BREAKS_STREAK`: A reference event outside tol breaks the streak and clears lock.
- `P_RESET_REACQUIRE`: Active-low reset clears stored edge history, streak, and lock and requires a fresh post-reset acquisition.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `lock_detector.va`.
Do not add or omit artifacts.
