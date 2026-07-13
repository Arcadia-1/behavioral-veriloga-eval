# Lock Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lock_detector.va`: `lock_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ALIGNMENT_STREAK`: lock asserts only after need consecutive reference edges whose most recent feedback edge is within tol.
- `P_PREMATURE_LOCK`: lock remains low before the need-th consecutive aligned reference event.
- `P_MISS_BREAKS_STREAK`: A reference event outside tol breaks the streak and clears lock.
- `P_RESET_REACQUIRE`: Active-low reset clears stored edge history, streak, and lock and requires a fresh post-reset acquisition.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lock_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
