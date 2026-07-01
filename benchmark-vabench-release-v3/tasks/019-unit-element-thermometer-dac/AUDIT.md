# Audit: 019 Unit Element Thermometer DAC

Gate 1: `independent_l1_ready`. This is the canonical unit-element thermometer
DAC row. It is independent from binary and segmented DAC rows because the
output is determined by active segment count, including the final segment.

Gate 2: `cadence_modeling_ready`. The public prompt states the 15 segment
ports, voltage thresholding rule, endpoint mapping by active count, transition
smoothing, and voltage-only constraints. Current PR validation: EVAS gold PASS,
Spectre AX hidden gold PASS, and EVAS/Spectre negatives rejected with no
Spectre errors. Spectre emitted only environment/setup warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck covers zero, partial, high-count, and full-scale segment counts.

Checker coverage: `v3_019_unit_element_thermometer_dac` enforces the public
unit-count transfer function and rejects gain error, nonlinear weighting,
inverted count, missing final segment, and scaling mistakes.
