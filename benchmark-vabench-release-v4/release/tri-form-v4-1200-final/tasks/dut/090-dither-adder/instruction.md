# Dither Adder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dither_adder.va`: `dither_adder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_POSITIVE_DITHER`: When DPN is above vth, the output differential exceeds the input differential by DITHER_AMP.
- `P_NEGATIVE_DITHER`: When DPN is at or below vth, the output differential is lower than the input differential by DITHER_AMP.
- `P_SYMMETRIC_SPLIT`: Half of the selected differential dither is added to VOUT_P and half is subtracted from VOUT_N.
- `P_COMMON_MODE_PRESERVATION`: The output pair preserves the input common mode and does not introduce a vdd/2 offset.
- `P_PARAMETER_OVERRIDE`: Legal DITHER_AMP and vth overrides change only dither magnitude and polarity decision as declared.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dither_adder.va`.
Do not add or omit artifacts.
