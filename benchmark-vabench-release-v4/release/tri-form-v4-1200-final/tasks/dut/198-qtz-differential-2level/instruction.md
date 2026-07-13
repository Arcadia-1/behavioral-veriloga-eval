# QTZ Differential 2level

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `qtz_differential_2level.va`: `qtz_differential_2level`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_SIGNED_CODE`: Initialize the signed output code to `-0.5`.
- `P_DIFFERENTIAL_MIDPOINT_DECISION`: On each rising `clk`, compare `vinp-vinn` with the midpoint between `vrefn` and `vrefp`.
- `P_BIPOLAR_TWO_LEVEL_OUTPUT`: Drive `dout` to the signed `+0.5` or `-0.5` level rather than a unipolar code.
- `P_CLOCKED_OUTPUT_HOLD`: Between rising clock decisions, hold the previous quantized output value.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `qtz_differential_2level.va`.
Do not add or omit artifacts.
