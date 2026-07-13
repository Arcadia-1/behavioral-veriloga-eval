# Dual Modulus Divider 16 17

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dual_modulus_divider_16_17.va`: `dual_modulus_divider_16_17`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MC_SELECTS_MODULUS`: `mc` selects divide-by-16 when low and divide-by-17 when high for rising `fin` crossings.
- `P_DIVIDE_COUNT_TIMING`: The output counter resets only at the terminal count for the selected modulus.
- `P_OUTPUT_LOW_MARKER_AND_LEVEL`: `fout` uses the specified low-marker count and declared voltage-coded output levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dual_modulus_divider_16_17.va`.
Do not add or omit artifacts.
