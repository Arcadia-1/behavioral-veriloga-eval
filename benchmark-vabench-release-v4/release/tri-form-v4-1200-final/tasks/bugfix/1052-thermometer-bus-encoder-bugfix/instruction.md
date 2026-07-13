# Thermometer Bus Encoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `thermometer_bus_encoder.va`: `thermometer_bus_encoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PREFIX_CODE`: Active segment outputs always form a contiguous prefix beginning at t0; no higher segment may be high while a lower segment is low.
- `P_ORDERED_ACTIVATION`: As vin increases, segments activate in order t0 through t15 and the active-segment count never decreases.
- `P_UNIFORM_SEGMENTS`: The clipped 0-to-vref input span selects among sixteen equal-width thermometer segments.
- `P_INPUT_CLIPPING`: Inputs at or below 0 V produce no active segments, and inputs at or above vref produce all sixteen active segments.
- `P_OUTPUT_LEVELS`: Each inactive segment approaches 0 V and each active segment approaches vh with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `thermometer_bus_encoder.va`.
Every supplied `.va` file is editable; do not add or omit files.
