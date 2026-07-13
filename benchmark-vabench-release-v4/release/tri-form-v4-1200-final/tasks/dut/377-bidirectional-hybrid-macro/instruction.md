# Bidirectional Hybrid Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bidirectional_hybrid_macro.va`: `bidirectional_hybrid_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEAR`: Reset centers the continuous sum and difference outputs and clears sampled metrics and balance qualification.
- `P_SUM_DIFF_MAPPING`: sum_out and diff_out implement the clipped common and differential mappings of port_a and port_b around vcm.
- `P_TRIM_RESPONSE`: The signed three-bit trim correction shifts sum and difference in opposite directions by trim_lsb per code.
- `P_DIRECTIONAL_METRICS`: At rising clock edges forward and reverse metrics reconstruct the directional components from the mapped sum and difference outputs.
- `P_BALANCE_QUALIFICATION`: balance_ok asserts only after two consecutive metric updates whose directional mismatch is within balance_tol.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bidirectional_hybrid_macro.va`.
Do not add or omit artifacts.
