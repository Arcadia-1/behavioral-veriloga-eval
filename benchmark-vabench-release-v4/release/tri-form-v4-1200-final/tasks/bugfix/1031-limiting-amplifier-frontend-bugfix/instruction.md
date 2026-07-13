# Limiting Amplifier Frontend Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `limiting_amplifier_frontend.va`: `limiting_amplifier_frontend`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_RESET_COMMON_MODE`: Initialization sets out to 0.45 V and metric to 0 V; an active-high reset sampled on a rising clk crossing restores the same state.
- `P_LINEAR_REGION`: For sampled input deviation from -0.09 V through 0.09 V, out equals 0.45 V plus 1.7 times the deviation and metric is 0 V.
- `P_POSITIVE_LIMITING`: Above the positive boundary, out follows 0.73 V plus 0.45 times excess deviation and metric is 0.85 V.
- `P_NEGATIVE_LIMITING`: Below the negative boundary, out follows 0.17 V plus 0.45 times excess negative deviation and metric is 0.85 V.
- `P_OUTPUT_CLAMP`: The final held output remains within 0.04 V through 0.86 V.
- `P_CLOCKED_HOLD`: Out and metric update only on rising clock crossings and hold between samples.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `limiting_amplifier_frontend.va`.
Every supplied `.va` file is editable; do not add or omit files.
