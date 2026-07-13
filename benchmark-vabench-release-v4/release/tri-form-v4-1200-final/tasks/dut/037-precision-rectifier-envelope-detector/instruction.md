# Precision Rectifier Envelope Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `precision_rectifier_envelope_detector.va`: `precision_rectifier_envelope_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FULL_WAVE_RECTIFICATION`: Rect equals vcm plus the absolute input deviation from vcm, so equal positive and negative excursions produce equal rectified levels, bounded to 0 V through 0.9 V.
- `P_RESET_ENVELOPE`: Initialization or a rising clk update with rst active restores env to vcm and clears envelope memory.
- `P_PEAK_ATTACK`: At a rising clk update, a rectified value above the stored envelope is acquired immediately as the new env value.
- `P_BOUNDED_DECAY`: When rect is below the stored envelope, each rising clk update lowers env by at most decay and never below rect or vcm.
- `P_ENVELOPE_LAG_METRIC`: Metric is high while env exceeds rect by more than 30 mV and low otherwise.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `precision_rectifier_envelope_detector.va`.
Do not add or omit artifacts.
