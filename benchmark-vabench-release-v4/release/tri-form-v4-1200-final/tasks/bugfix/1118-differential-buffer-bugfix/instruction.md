# Differential Buffer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `differential_buffer.va`: `differential_buffer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_POSITIVE_UNITY`: VOUTP continuously follows VINP with unity voltage gain and unchanged polarity.
- `P_NEGATIVE_UNITY`: VOUTN continuously follows VINN with unity voltage gain and unchanged polarity.
- `P_CHANNEL_INDEPENDENCE`: Each output depends on its corresponding input and is not cross-coupled to the opposite input.
- `P_DIFFERENTIAL_PRESERVATION`: The differential output VOUTP minus VOUTN equals the differential input VINP minus VINN.
- `P_COMMON_MODE_PRESERVATION`: The output pair preserves the input pair common-mode voltage without conversion or rail logic.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `differential_buffer.va`.
Every supplied `.va` file is editable; do not add or omit files.
