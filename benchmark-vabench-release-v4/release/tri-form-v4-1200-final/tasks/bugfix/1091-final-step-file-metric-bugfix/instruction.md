# Final Step File Metric Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `final_step_file_metric_ref.va`: `final_step_file_metric_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ZERO_INITIAL_STATE`: Before any qualifying ref edge, the event count and metric_out are zero.
- `P_RISING_EDGE_COUNT`: Every rising ref crossing through vth increments the retained event count exactly once; falling crossings do not.
- `P_NORMALIZED_METRIC`: Metric_out equals the VDD-to-VSS rail span multiplied by the retained event count divided by four.
- `P_EVENT_UPDATED_OUTPUT`: Metric_out changes only after counted rising events and uses finite transition smoothing of the retained target.
- `P_FINAL_TEXT_RECORD`: At final_step, the module emits one text metric record to candidate.out in the simulator working directory with format count=<integer> metric=<fixed-point to three decimals>.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `final_step_file_metric_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
