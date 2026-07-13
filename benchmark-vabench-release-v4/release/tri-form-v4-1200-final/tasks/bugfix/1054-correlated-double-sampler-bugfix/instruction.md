# Correlated Double Sampler Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `correlated_double_sampler.va`: `correlated_double_sampler`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_SAMPLE`: A rising phi_reset crossing captures vin as the reset level, returns vout to vcm, and clears valid.
- `P_SIGNAL_CORRECTION`: A rising phi_signal crossing publishes vcm plus gain times the current signal sample minus the most recently captured reset sample.
- `P_OUTPUT_CLAMP`: The corrected output is limited to the inclusive vlo-to-vhi range.
- `P_VALID_SEQUENCE`: valid is low before a completed signal sample and after every reset sample, then rises to vhi when a signal sample is published.
- `P_HOLD_BETWEEN_EVENTS`: vout and valid hold their last event-updated states between reset and signal sampling crossings.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `correlated_double_sampler.va`.
Every supplied `.va` file is editable; do not add or omit files.
