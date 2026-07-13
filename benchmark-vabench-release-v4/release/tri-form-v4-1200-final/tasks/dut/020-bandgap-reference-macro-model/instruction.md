# Bandgap Reference Macro Model

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bandgap_reference_macro_model.va`: `bandgap_reference_macro_model`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_AND_BROWNOUT`: Reset or vin below vstart forces out and metric to 0 V.
- `P_CLOCKED_FIRST_ORDER_SETTLING`: On eligible rising clock crossings, the held reference advances by 0.35 of the remaining error to the clamped line-corrected target.
- `P_TARGET_AND_OUTPUT_CLAMPS`: The line-corrected target is clamped to 0 through vin minus 0.05 V, and driven out remains within 0 through 0.9 V.
- `P_VALIDITY_ENCODING`: Metric is 0 V in reset or brownout, 0.2 V during startup below the 0.48 V validity threshold, and 0.9 V after the held reference exceeds it.
- `P_CLOCKED_HOLD`: Above startup, the reference state changes only on rising clock crossings and holds between samples.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bandgap_reference_macro_model.va`.
Do not add or omit artifacts.
