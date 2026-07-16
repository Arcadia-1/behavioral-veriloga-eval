# Rail Normalized Metric Mapper Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.

## Public Verilog-A Interface

Preserve this exact artifact and module interface:

- Artifact `rail_normalized_metric_mapper.va`:
  - Module `rail_normalized_metric_mapper` (entry)
    - position 0: `meas` (input, electrical)
    - position 1: `vdd` (input, electrical)
    - position 2: `vss` (input, electrical)
    - position 3: `en` (input, electrical)
    - position 4: `norm` (output, electrical)
    - position 5: `valid` (output, electrical)

## Public Parameter Contract

- `rail_normalized_metric_mapper.vth` defaults to `0.45`; valid range: finite; overrides vth.
- `rail_normalized_metric_mapper.vhi` defaults to `0.9`; valid range: finite; overrides vhi.
- `rail_normalized_metric_mapper.span_min` defaults to `0.60`; valid range: finite; overrides span_min.
- `rail_normalized_metric_mapper.span_max` defaults to `1.20`; valid range: finite; overrides span_max.
- `rail_normalized_metric_mapper.tr` defaults to `50p`; valid range: finite; overrides tr.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_NORMALIZE_MEAS_RELATIVE_TO_THE_LOCAL`: restore: Let `span = V(vdd, vss)` and `local_meas = V(meas) - V(vss)`. When `V(en) > vth` and `span >= span_min`, `norm = vhi * clip01(local_meas / span)`. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_CLIP_THE_NORMALIZED_METRIC_TO_THE`: restore: `clip01(x)` limits `x` to `[0, 1]`, so enabled `norm` is clipped to `[0 V, vhi]` even when `meas` lies outside the local rails. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_ASSERT_VALID_ONLY_WHEN_ENABLE_IS`: restore: `valid = vhi` exactly when `V(en) > vth`, `span_min <= span <= span_max`, and `0 <= local_meas <= span`; otherwise `valid = 0 V`. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_CLEAR_NORM_AND_VALID_WHILE_DISABLED`: restore: Disabled or `span < span_min` clears both outputs. A span above `span_max` clears `valid` but does not by itself clear clipped `norm`. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: restore: Use local analog helper functions rather than user task/endtask syntax. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.

## Modeling Constraints

- Use deterministic voltage-domain behavioral Verilog-A.
- Do not hard-code validation stimulus, stop times, sample windows, gold internals, or simulator side channels.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these paths: `rail_normalized_metric_mapper.va`.
Every supplied `.va` file is editable; do not add or omit files.
