# Quadrature Phase Interpolator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `quadrature_phase_interpolator.va`: `quadrature_phase_interpolator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_CLEAR_CLK_OUT_QUADRANT`: On reset, clear `clk_out`, quadrant outputs, and `phase_metric`.
- `P_OBSERVE_THE_RISING_EDGES_OF_CLK`: Observe the rising edges of `clk_i` and `clk_q` and maintain a four-quadrant phase reference.
- `P_DECODE_CODE_4_CODE_0_AS`: Decode `code_4..code_0` as an unsigned phase code from 0 to 31.
- `P_GENERATE_CLK_OUT_EDGES_DELAYED_FROM`: Generate `clk_out` edges delayed from the selected quadrant reference by `unit_delay` times the intra-quadrant code.
- `P_QUADRANT_1_QUADRANT_0_MUST_EXPOSE`: `quadrant_1..quadrant_0` must expose the selected quadrant.
- `P_PHASE_METRIC_MUST_EXPOSE_THE_DECODED`: `phase_metric` must expose the decoded phase code as a voltage-level metric.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `quadrature_phase_interpolator.va`.
Do not add or omit artifacts.
