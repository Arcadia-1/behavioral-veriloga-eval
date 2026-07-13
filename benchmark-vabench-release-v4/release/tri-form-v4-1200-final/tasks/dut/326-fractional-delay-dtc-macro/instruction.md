# Fractional-delay DTC Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `fractional_delay_dtc_macro.va`: `fractional_delay_dtc_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, phase metric, and `valid`.
- `P_DECODE_FRAC_3_FRAC_0_AS`: Decode `frac_3..frac_0` as a fractional delay setting.
- `P_FOR_EACH_INPUT_EDGE_EMIT_ONE`: For each input edge, emit one output edge with a delay proportional to the fractional code.
- `P_EXPOSE_THE_FRACTIONAL_DELAY_AS_PHASE`: Expose the fractional delay as `phase_metric`.
- `P_PRESERVE_INPUT_EDGE_ORDER_AND_ASSERT`: Preserve input-edge order and assert `valid` after the first emitted delayed edge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `fractional_delay_dtc_macro.va`.
Do not add or omit artifacts.
