# Final Step File Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `final_step_file_metric_ref.va`: `final_step_file_metric_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ZERO_INITIAL_STATE`: Before any qualifying ref edge, the event count and metric_out are zero.
- `P_RISING_EDGE_COUNT`: Every rising ref crossing through vth increments the retained event count exactly once; falling crossings do not.
- `P_NORMALIZED_METRIC`: Metric_out equals the VDD-to-VSS rail span multiplied by the retained event count divided by four.
- `P_EVENT_UPDATED_OUTPUT`: Metric_out changes only after counted rising events and uses finite transition smoothing of the retained target.
- `P_FINAL_TEXT_RECORD`: At final_step, the module emits one text metric record to candidate.out in the simulator working directory with format count=<integer> metric=<fixed-point to three decimals>.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `final_step_file_metric_ref.va`.
Do not add or omit artifacts.
