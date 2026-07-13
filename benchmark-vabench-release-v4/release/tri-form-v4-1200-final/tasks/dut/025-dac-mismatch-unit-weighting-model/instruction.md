# DAC Mismatch Unit Weighting Model

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_mismatch_unit_weighting_model.va`: `dac_mismatch_unit_weighting_model`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ZERO_AND_FULL_SCALE`: All-zero input maps to vlo and all-active input maps to vhi after transition settling.
- `P_NONIDEAL_WEIGHT_SUM`: Inputs b0 through b3 contribute fixed positive weights 1.00, 2.02, 3.96, and 8.08 normalized by their all-active sum.
- `P_LOGIC_THRESHOLD`: Each bit is independently interpreted using the public fixed 0.45 V decision threshold.
- `P_BOUNDED_OUTPUT`: For every input pattern, the settled output remains within the vlo-to-vhi interval.
- `P_MISMATCH_OBSERVABILITY`: Single-bit output increments preserve the stated nonideal weighting rather than ideal powers-of-two weighting.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_mismatch_unit_weighting_model.va`.
Do not add or omit artifacts.
