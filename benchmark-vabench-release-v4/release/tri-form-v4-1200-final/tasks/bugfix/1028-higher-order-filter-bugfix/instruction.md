# Clocked Cascaded Two-Pole Filter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `higher_order_filter.va`: `higher_order_filter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_COMMON_MODE_INITIAL_RESET`: Both cascaded states and observable out return to 0.45 V during initialization and active-high reset.
- `P_GAINED_BOUNDED_TARGET`: Each eligible rising edge forms a rail-bounded target from gain times the input deviation around 0.45 V.
- `P_TWO_POLE_SAMPLED_SETTLING`: Out follows the second of two cascaded alpha-weighted sampled low-pass states and therefore settles more slowly than a single direct update.
- `P_LAG_METRIC`: Metric exposes the centered lag between the two cascaded states during settling and returns toward its baseline after convergence.
- `P_SIGNAL_RANGE`: The driven output remains within the public 0 V through 0.9 V signal range.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `higher_order_filter.va`.
Every supplied `.va` file is editable; do not add or omit files.
