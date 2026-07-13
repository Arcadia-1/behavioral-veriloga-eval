# Binary Weighted Voltage DAC Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `simple_binary_voltage_dac_4b.va`: `simple_binary_voltage_dac_4b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_BINARY_WEIGHTS`: code_0 through code_3 form an unsigned four-bit word with weights one, two, four, and eight.
- `P_ENDPOINTS`: Code zero maps to vss and code fifteen maps to vref.
- `P_LINEAR_MONOTONIC_MAPPING`: aout changes linearly and monotonically with the unsigned code between the rail endpoints.
- `P_CONTINUOUS_UPDATE`: aout responds continuously to code-bit changes without a clock event.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `simple_binary_voltage_dac_4b.va`.
Every supplied `.va` file is editable; do not add or omit files.
