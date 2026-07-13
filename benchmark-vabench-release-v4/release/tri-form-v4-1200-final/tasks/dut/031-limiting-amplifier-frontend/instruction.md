# Limiting Amplifier Frontend

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `limiting_amplifier_frontend.va`: `limiting_amplifier_frontend`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_RESET_COMMON_MODE`: Initialization sets out to 0.45 V and metric to 0 V; an active-high reset sampled on a rising clk crossing restores the same state.
- `P_LINEAR_REGION`: For sampled input deviation from -0.09 V through 0.09 V, out equals 0.45 V plus 1.7 times the deviation and metric is 0 V.
- `P_POSITIVE_LIMITING`: Above the positive boundary, out follows 0.73 V plus 0.45 times excess deviation and metric is 0.85 V.
- `P_NEGATIVE_LIMITING`: Below the negative boundary, out follows 0.17 V plus 0.45 times excess negative deviation and metric is 0.85 V.
- `P_OUTPUT_CLAMP`: The final held output remains within 0.04 V through 0.86 V.
- `P_CLOCKED_HOLD`: Out and metric update only on rising clock crossings and hold between samples.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `limiting_amplifier_frontend.va`.
Do not add or omit artifacts.
