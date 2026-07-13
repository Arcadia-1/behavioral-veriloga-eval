# Slew Rate DAC4 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `slew_rate_dac4.va`: `slew_rate_dac4`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_BINARY_MAPPING`: d3 is the MSB and d0 is the LSB of an unsigned four-bit code whose target output is binary weighted.
- `P_ENDPOINTS`: Code 0 targets 0 V and code 15 targets vref.
- `P_CODE_MONOTONICITY`: A larger stable input code does not produce a lower settled output voltage.
- `P_SLEW_LIMIT`: During a target change, the magnitude of the output slope does not exceed slewrate.
- `P_SETTLED_TARGET`: After sufficient time at a stable code, vout reaches the corresponding code-to-vref target.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `slew_rate_dac4.va`.
Every supplied `.va` file is editable; do not add or omit files.
