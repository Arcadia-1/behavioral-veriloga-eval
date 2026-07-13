# Binary Weighted Voltage DAC

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `simple_binary_voltage_dac_4b.va`: `simple_binary_voltage_dac_4b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_BINARY_WEIGHTS`: code_0 through code_3 form an unsigned four-bit word with weights one, two, four, and eight.
- `P_ENDPOINTS`: Code zero maps to vss and code fifteen maps to vref.
- `P_LINEAR_MONOTONIC_MAPPING`: aout changes linearly and monotonically with the unsigned code between the rail endpoints.
- `P_CONTINUOUS_UPDATE`: aout responds continuously to code-bit changes without a clock event.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `simple_binary_voltage_dac_4b.va`.
Do not add or omit artifacts.
