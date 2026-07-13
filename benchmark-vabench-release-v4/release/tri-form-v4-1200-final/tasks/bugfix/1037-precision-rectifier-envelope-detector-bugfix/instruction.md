# Precision Rectifier Envelope Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `precision_rectifier_envelope_detector.va`: `precision_rectifier_envelope_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FULL_WAVE_RECTIFICATION`: Rect equals vcm plus the absolute input deviation from vcm, so equal positive and negative excursions produce equal rectified levels, bounded to 0 V through 0.9 V.
- `P_RESET_ENVELOPE`: Initialization or a rising clk update with rst active restores env to vcm and clears envelope memory.
- `P_PEAK_ATTACK`: At a rising clk update, a rectified value above the stored envelope is acquired immediately as the new env value.
- `P_BOUNDED_DECAY`: When rect is below the stored envelope, each rising clk update lowers env by at most decay and never below rect or vcm.
- `P_ENVELOPE_LAG_METRIC`: Metric is high while env exceeds rect by more than 30 mV and low otherwise.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `precision_rectifier_envelope_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
