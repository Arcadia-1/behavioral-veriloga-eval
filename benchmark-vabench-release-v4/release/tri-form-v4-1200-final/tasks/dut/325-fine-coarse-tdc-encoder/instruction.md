# Fine/coarse TDC Encoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `fine_coarse_tdc_encoder_top.va`: `fine_coarse_tdc_encoder_top`
- `coarse_counter.va`: `coarse_counter`
- `fine_residual_metric.va`: `fine_residual_metric`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear coarse code, fine metric, and `valid`.
- `P_A_RISING_START_EDGE_ARMS_A`: A rising `start` edge arms a measurement and clears the coarse counter.
- `P_COUNT_RISING_REF_CLK_EDGES_UNTIL`: Count rising `ref_clk` edges until the first rising `stop` edge.
- `P_LATCH_THE_COARSE_COUNT_INTO_COARSE`: Latch the coarse count into `coarse_3..coarse_0` and expose a fine residual proxy on `fine_metric`.
- `P_ASSERT_VALID_ONLY_AFTER_THE_STOP`: Assert `valid` only after the stop edge completes the measurement.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `fine_coarse_tdc_encoder_top.va`, `coarse_counter.va`, `fine_residual_metric.va`.
Do not add or omit artifacts.
