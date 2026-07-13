# DWA DEM Encoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dwa_ptr_gen.va`: `dwa_ptr_gen`
- `v2b_4b.va`: `v2b_4b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_V2B_ROUND_AND_CLAMP`: On each rising helper clock crossing, vin rounds to the nearest integer and clamps to a four-bit code from 0 through 15.
- `P_ACTIVE_LOW_RESET_POINTER`: A sampled active-low reset initializes ptr to the one-hot ptr_init position.
- `P_ROTATING_POINTER_UPDATE`: Each post-reset rising edge advances the circular pointer by the sampled unsigned code modulo 16.
- `P_POINTER_ONE_HOT`: Ptr remains exactly one-hot at the updated circular pointer position.
- `P_DWA_SELECTED_MASK`: Cell_en implements the public rotating span and LSB boundary-cell rule for the sampled code, including the code-zero boundary-cell case.
- `P_SYSTEM_CODE_BINDING`: The four helper outputs feed the DWA code bus in MSB-to-LSB order without bit reversal.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dwa_ptr_gen.va`, `v2b_4b.va`.
Do not add or omit artifacts.
