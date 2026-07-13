# Divide By Two Toggle Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `divide_by_two_toggle.va`: `divide_by_two_toggle`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_TOGGLE_STATE`: Each rising `clkin` crossing through 0.5 V toggles the retained divider state.
- `P_INITIAL_LOW_STATE`: The retained state and `clkout` start low before the first input-clock edge.
- `P_OUTPUT_RAIL_LEVELS`: `clkout` drives 0.9 V for high state and 0.0 V for low state without amplitude scaling.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `divide_by_two_toggle.va`.
Every supplied `.va` file is editable; do not add or omit files.
