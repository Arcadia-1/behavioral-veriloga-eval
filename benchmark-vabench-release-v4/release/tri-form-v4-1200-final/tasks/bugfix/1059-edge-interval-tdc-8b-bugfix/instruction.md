# Edge Interval TDC 8b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `edge_interval_tdc_8b.va`: `edge_interval_tdc_8b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_START_ARMS`: Each rising start crossing begins a new interval measurement, records that edge time, and clears valid.
- `P_NEXT_STOP_COMPLETES`: The first rising stop crossing after an armed start completes that measurement; stop crossings while unarmed do not change the result.
- `P_INTERVAL_QUANTIZATION`: A completed interval is rounded to the nearest whole nanosecond and reported as an unsigned code.
- `P_CODE_SATURATION`: Measured interval codes are saturated to the inclusive 8-bit range 0 through 255.
- `P_VALID_AND_BIT_ORDER`: valid asserts after completion; code0 is the least significant bit and code7 is the most significant bit, using 0 V and vdd logic levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `edge_interval_tdc_8b.va`.
Every supplied `.va` file is editable; do not add or omit files.
