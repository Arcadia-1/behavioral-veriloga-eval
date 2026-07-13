# Differential Buffer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `differential_buffer.va`: `differential_buffer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_POSITIVE_UNITY`: VOUTP continuously follows VINP with unity voltage gain and unchanged polarity.
- `P_NEGATIVE_UNITY`: VOUTN continuously follows VINN with unity voltage gain and unchanged polarity.
- `P_CHANNEL_INDEPENDENCE`: Each output depends on its corresponding input and is not cross-coupled to the opposite input.
- `P_DIFFERENTIAL_PRESERVATION`: The differential output VOUTP minus VOUTN equals the differential input VINP minus VINN.
- `P_COMMON_MODE_PRESERVATION`: The output pair preserves the input pair common-mode voltage without conversion or rail logic.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `differential_buffer.va`.
Do not add or omit artifacts.
