# Settling Window Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `settling_window_detector.va`: `settling_window_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_WINDOW_DEFINITION`: The input is qualified in-window exactly while the absolute vin-to-target error is no greater than tol.
- `P_ENTRY_AND_HOLD`: Entering the window records the entry time, but settled remains low until vin has stayed continuously in-window for at least 20 ns.
- `P_EXIT_RESETS_QUALIFICATION`: Leaving the tolerance window before or after qualification clears the entry state, drives settled low, and clears the time code.
- `P_ENTRY_TIME_CODE`: After qualification, t_code[7:0] reports the rounded window-entry time in whole nanoseconds, saturated to 0 through 255.
- `P_BIT_ORDER_AND_LEVELS`: t_code0 is the least significant bit and t_code7 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `settling_window_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
