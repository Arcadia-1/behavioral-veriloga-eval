# Gain Estimator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `gain_estimator.va`: `gain_estimator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_START_TIME_GATING`: Samples before start_time do not contribute to measured input or output extrema and valid remains low.
- `P_PERIODIC_EXTREMA`: At each sample_period after start_time, the estimator updates minima and maxima of the input and output differential voltages.
- `P_VALIDITY_THRESHOLD`: Valid remains rail-low until the observed input differential span exceeds min_input_span and remains rail-high afterwards.
- `P_SPAN_RATIO`: Once valid, the measured gain equals output differential span divided by input differential span.
- `P_NORMALIZED_GAIN_OUTPUT`: Gain_out equals the VDD-to-VSS rail span multiplied by measured gain divided by gain_scale.
- `P_EVENT_UPDATED_TARGETS`: Gain_out and valid reflect event-updated retained targets with finite smoothing rather than continuously varying transition inputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `gain_estimator.va`.
Every supplied `.va` file is editable; do not add or omit files.
