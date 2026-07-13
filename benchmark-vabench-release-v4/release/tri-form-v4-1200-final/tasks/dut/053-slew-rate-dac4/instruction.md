# Slew Rate DAC4

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `slew_rate_dac4.va`: `slew_rate_dac4`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_BINARY_MAPPING`: d3 is the MSB and d0 is the LSB of an unsigned four-bit code whose target output is binary weighted.
- `P_ENDPOINTS`: Code 0 targets 0 V and code 15 targets vref.
- `P_CODE_MONOTONICITY`: A larger stable input code does not produce a lower settled output voltage.
- `P_SLEW_LIMIT`: During a target change, the magnitude of the output slope does not exceed slewrate.
- `P_SETTLED_TARGET`: After sufficient time at a stable code, vout reaches the corresponding code-to-vref target.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `slew_rate_dac4.va`.
Do not add or omit artifacts.
