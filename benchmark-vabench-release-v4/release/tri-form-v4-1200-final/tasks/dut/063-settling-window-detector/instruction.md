# Settling Window Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `settling_window_detector.va`: `settling_window_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_WINDOW_DEFINITION`: The input is qualified in-window exactly while the absolute vin-to-target error is no greater than tol.
- `P_ENTRY_AND_HOLD`: Entering the window records the entry time, but settled remains low until vin has stayed continuously in-window for at least 20 ns.
- `P_EXIT_RESETS_QUALIFICATION`: Leaving the tolerance window before or after qualification clears the entry state, drives settled low, and clears the time code.
- `P_ENTRY_TIME_CODE`: After qualification, t_code[7:0] reports the rounded window-entry time in whole nanoseconds, saturated to 0 through 255.
- `P_BIT_ORDER_AND_LEVELS`: t_code0 is the least significant bit and t_code7 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `settling_window_detector.va`.
Do not add or omit artifacts.
