# Flash Data Align Pipeline

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `flash_data_align_pipeline.va`: `flash_data_align_pipeline`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_THERMOMETER_COUNT`: At each rising `clk` crossing through `vth`, count all asserted thermometer inputs `din0` through `din7`.
- `P_FOUR_STAGE_ALIGNMENT`: The sampled count is shifted through a four-stage alignment pipeline before it is published.
- `P_BINARY_OUTPUT_ORDER`: The delayed count is driven as voltage-coded binary with `dout0` as LSB and `dout3` as MSB.
- `P_EVENT_HELD_OUTPUTS`: Outputs update only from pipeline clock events and hold their previous voltage-coded state between events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `flash_data_align_pipeline.va`.
Do not add or omit artifacts.
