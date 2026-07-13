# Safe Analog Divider

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `safe_analog_divider.va`: `safe_analog_divider`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_USE_V_SIGDENOM_DIRECTLY_WHEN_ITS`: For denominator magnitudes at least `min_sigdenom`, use `V(sigdenom)` directly in the divider transfer.
- `P_WHEN_V_SIGDENOM_IS_POSITIVE_BUT`: For positive denominator magnitudes below `min_sigdenom`, use `+min_sigdenom` as the guarded denominator.
- `P_WHEN_V_SIGDENOM_IS_EXACTLY_ZERO`: For exactly zero denominator, use `+min_sigdenom` as the guarded denominator.
- `P_WHEN_V_SIGDENOM_IS_NEGATIVE_BUT`: For negative denominator magnitudes below `min_sigdenom`, use `-min_sigdenom` as the guarded denominator.
- `P_DRIVE_SIGOUT_TO_GAIN_V_SIGNUMER`: Drive `sigout` to the observable transfer `gain * V(signumer) / guarded_denominator`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `safe_analog_divider.va`.
Do not add or omit artifacts.
