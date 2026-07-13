# Threshold Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `comparator.va`: `comparator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_DECISION`: At initialization, OUT_P reflects the sign of VINP minus VINN.
- `P_RISING_DIFFERENTIAL`: When VINP crosses above VINN, OUT_P transitions to the VDD rail.
- `P_FALLING_DIFFERENTIAL`: When VINP crosses below VINN, OUT_P transitions to the VSS rail.
- `P_BIDIRECTIONAL_RESPONSE`: Repeated differential crossings in either direction update the retained decision without requiring a clock or reset.
- `P_RAIL_SMOOTHING`: OUT_P is rail-referenced and changes with finite transition smoothing set by tedge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `comparator.va`.
Do not add or omit artifacts.
