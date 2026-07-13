# Quadrature LO Generator from Divided Clock

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `quadrature_lo_generator_divided_clock.va`: `quadrature_lo_generator_divided_clock`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears both LO outputs, state metric, and quad_ok.
- `P_QUADRATURE_SEQUENCE`: Enabled rising input edges drive the repeating 10, 11, 01, 00 sequence.
- `P_DIVIDE_BY_FOUR`: Each LO has one cycle per four input rising edges with equal frequency and deterministic quadrature order.
- `P_STATE_METRIC`: div_metric reports the currently driven sequence index as k/3 of the output span.
- `P_QUAD_OK_DELAY`: quad_ok asserts only after two complete four-state output cycles.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `quadrature_lo_generator_divided_clock.va`.
Do not add or omit artifacts.
