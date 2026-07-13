# Safe Analog Divider Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `safe_analog_divider.va`: `safe_analog_divider`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_USE_V_SIGDENOM_DIRECTLY_WHEN_ITS`: For denominator magnitudes at least `min_sigdenom`, use `V(sigdenom)` directly in the divider transfer.
- `P_WHEN_V_SIGDENOM_IS_POSITIVE_BUT`: For positive denominator magnitudes below `min_sigdenom`, use `+min_sigdenom` as the guarded denominator.
- `P_WHEN_V_SIGDENOM_IS_EXACTLY_ZERO`: For exactly zero denominator, use `+min_sigdenom` as the guarded denominator.
- `P_WHEN_V_SIGDENOM_IS_NEGATIVE_BUT`: For negative denominator magnitudes below `min_sigdenom`, use `-min_sigdenom` as the guarded denominator.
- `P_DRIVE_SIGOUT_TO_GAIN_V_SIGNUMER`: Drive `sigout` to the observable transfer `gain * V(signumer) / guarded_denominator`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `safe_analog_divider.va`.
Every supplied `.va` file is editable; do not add or omit files.
