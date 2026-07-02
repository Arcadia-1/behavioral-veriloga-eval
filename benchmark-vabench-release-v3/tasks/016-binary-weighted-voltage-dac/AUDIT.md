# Audit: 016 Binary Weighted Voltage DAC

Gate 1: `independent_l1_ready`. This is the canonical 4-bit binary voltage DAC
row. It remains useful as the simple endpoint-mapped baseline against which the
segmented, thermometer, mismatch, folded, and subradix DAC rows are distinct.

Gate 2: `cadence_modeling_ready`. The public prompt states the interface, bit
order, endpoint mapping, 4-bit binary transfer behavior, transition smoothing,
and voltage-only constraints. Current PR validation: EVAS gold PASS, Spectre AX
hidden gold PASS, and EVAS/Spectre negatives rejected with no Spectre errors.
Spectre emitted only environment/setup warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck exercises all codes, endpoint behavior, monotonicity, and bit
weights beyond visible smoke coverage.

Checker coverage: `v3_016_binary_weighted_voltage_dac` evaluates the public
binary transfer contract and rejects gain, bit-weight, bit-order, endpoint, and
saturation errors.
