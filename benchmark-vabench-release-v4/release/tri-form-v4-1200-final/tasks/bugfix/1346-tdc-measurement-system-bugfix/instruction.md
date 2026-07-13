# TDC Event Measurement System Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `tdc_measurement_top.va`: `tdc_measurement_top`
- `edge_detector.va`: `edge_detector`
- `interval_counter.va`: `interval_counter`
- `binary_encoder.va`: `binary_encoder`
- `valid_latch.va`: `valid_latch`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TDC_RESET_CLEAR`: Reset clears count code, valid, and overflow.
- `P_TDC_RESTART_CLEAR`: Each rising start edge begins a new interval and clears valid and overflow.
- `P_TDC_INTERVAL_COUNT`: The first stop after start latches the number of intervening rising clock edges.
- `P_TDC_VALID_LATCH`: A completed interval asserts valid and preserves its code until restart or reset.
- `P_TDC_OVERFLOW`: The 256th armed clock saturates code at 255, asserts overflow and valid, and disarms.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `tdc_measurement_top.va`, `edge_detector.va`, `interval_counter.va`, `binary_encoder.va`, `valid_latch.va`.
Every supplied `.va` file is editable; do not add or omit files.
