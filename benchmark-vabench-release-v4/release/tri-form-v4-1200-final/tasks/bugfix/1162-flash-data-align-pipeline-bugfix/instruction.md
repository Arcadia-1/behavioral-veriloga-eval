# Flash Data Align Pipeline Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `flash_data_align_pipeline.va`: `flash_data_align_pipeline`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_THERMOMETER_COUNT`: At each rising `clk` crossing through `vth`, count all asserted thermometer inputs `din0` through `din7`.
- `P_FOUR_STAGE_ALIGNMENT`: The sampled count is shifted through a four-stage alignment pipeline before it is published.
- `P_BINARY_OUTPUT_ORDER`: The delayed count is driven as voltage-coded binary with `dout0` as LSB and `dout3` as MSB.
- `P_EVENT_HELD_OUTPUTS`: Outputs update only from pipeline clock events and hold their previous voltage-coded state between events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `flash_data_align_pipeline.va`.
Every supplied `.va` file is editable; do not add or omit files.
