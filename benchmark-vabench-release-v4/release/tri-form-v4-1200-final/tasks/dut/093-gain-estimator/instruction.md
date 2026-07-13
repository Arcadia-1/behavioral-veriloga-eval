# Gain Estimator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `gain_estimator.va`: `gain_estimator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_START_TIME_GATING`: Samples before start_time do not contribute to measured input or output extrema and valid remains low.
- `P_PERIODIC_EXTREMA`: At each sample_period after start_time, the estimator updates minima and maxima of the input and output differential voltages.
- `P_VALIDITY_THRESHOLD`: Valid remains rail-low until the observed input differential span exceeds min_input_span and remains rail-high afterwards.
- `P_SPAN_RATIO`: Once valid, the measured gain equals output differential span divided by input differential span.
- `P_NORMALIZED_GAIN_OUTPUT`: Gain_out equals the VDD-to-VSS rail span multiplied by measured gain divided by gain_scale.
- `P_EVENT_UPDATED_TARGETS`: Gain_out and valid reflect event-updated retained targets with finite smoothing rather than continuously varying transition inputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `gain_estimator.va`.
Do not add or omit artifacts.
