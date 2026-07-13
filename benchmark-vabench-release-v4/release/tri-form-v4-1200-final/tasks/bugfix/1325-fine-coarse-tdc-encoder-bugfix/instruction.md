# Fine/coarse TDC Encoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `fine_coarse_tdc_encoder_top.va`: `fine_coarse_tdc_encoder_top`
- `coarse_counter.va`: `coarse_counter`
- `fine_residual_metric.va`: `fine_residual_metric`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear coarse code, fine metric, and `valid`.
- `P_A_RISING_START_EDGE_ARMS_A`: A rising `start` edge arms a measurement and clears the coarse counter.
- `P_COUNT_RISING_REF_CLK_EDGES_UNTIL`: Count rising `ref_clk` edges until the first rising `stop` edge.
- `P_LATCH_THE_COARSE_COUNT_INTO_COARSE`: Latch the coarse count into `coarse_3..coarse_0` and expose a fine residual proxy on `fine_metric`.
- `P_ASSERT_VALID_ONLY_AFTER_THE_STOP`: Assert `valid` only after the stop edge completes the measurement.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `fine_coarse_tdc_encoder_top.va`, `coarse_counter.va`, `fine_residual_metric.va`.
Every supplied `.va` file is editable; do not add or omit files.
