# Comparator Reset Low 1p8 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `comparator_reset_low_1p8.va`: `comparator_reset_low_1p8`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIALIZE_BOTH_DECISION_OUTPUTS_LOW_WHENEVER`: Initialize both decision outputs low. Whenever `cmpck` falls through `vdd/2`, reset both outputs low. Whenever `cmpck` rises through `vdd/2`, latch a differential decision: drive `dcmpp` high for `vinp > vinn`, drive `dcmpn` high for `vinp < vinn`, and keep both outputs low for an equal-input decision. Hold the latched or reset state until the next clock event.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `comparator_reset_low_1p8.va`.
Every supplied `.va` file is editable; do not add or omit files.
