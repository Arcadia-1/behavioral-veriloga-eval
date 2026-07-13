# TDC Event Measurement System

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `tdc_measurement_top.va`: `tdc_measurement_top`
- `edge_detector.va`: `edge_detector`
- `interval_counter.va`: `interval_counter`
- `binary_encoder.va`: `binary_encoder`
- `valid_latch.va`: `valid_latch`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TDC_RESET_CLEAR`: Reset clears count code, valid, and overflow.
- `P_TDC_RESTART_CLEAR`: Each rising start edge begins a new interval and clears valid and overflow.
- `P_TDC_INTERVAL_COUNT`: The first stop after start latches the number of intervening rising clock edges.
- `P_TDC_VALID_LATCH`: A completed interval asserts valid and preserves its code until restart or reset.
- `P_TDC_OVERFLOW`: The 256th armed clock saturates code at 255, asserts overflow and valid, and disarms.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `tdc_measurement_top.va`, `edge_detector.va`, `interval_counter.va`, `binary_encoder.va`, `valid_latch.va`.
Do not add or omit artifacts.
