# Quadrature LO Generator from Divided Clock Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `quadrature_lo_generator_divided_clock.va`: `quadrature_lo_generator_divided_clock`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears both LO outputs, state metric, and quad_ok.
- `P_QUADRATURE_SEQUENCE`: Enabled rising input edges drive the repeating 10, 11, 01, 00 sequence.
- `P_DIVIDE_BY_FOUR`: Each LO has one cycle per four input rising edges with equal frequency and deterministic quadrature order.
- `P_STATE_METRIC`: div_metric reports the currently driven sequence index as k/3 of the output span.
- `P_QUAD_OK_DELAY`: quad_ok asserts only after two complete four-state output cycles.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `quadrature_lo_generator_divided_clock.va`.
Every supplied `.va` file is editable; do not add or omit files.
