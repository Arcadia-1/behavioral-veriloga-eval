# Audit: 113 Clocked DAC Restore 4b

Gate 1: `independent_l1_ready`. This is a clocked 4-bit mid-rise bipolar DAC
restore model. It is not counted as merely another binary voltage DAC because
the public behavior is sampled on the clock, uses a bipolar mid-rise transfer,
and holds the reconstructed level between updates.

Gate 2: `cadence_modeling_ready`. The public prompt states the interface, bit
order, rising-clock sampling, mid-rise half-LSB offset, nominal output range,
hold behavior, transition smoothing, and voltage-only constraints. Current PR
validation: EVAS gold PASS, Spectre AX hidden gold PASS, and EVAS/Spectre
negatives rejected with no Spectre errors. Spectre emitted only
environment/setup warnings.

Hidden/visible coverage: repaired in this PR. The hidden deck now uses a
different monotonic code sequence from the visible smoke deck, so hidden
coverage is no longer byte-identical to visible coverage.

Checker coverage: `v3_clocked_dac_restore_4b` checks private stable samples
against the public mid-rise transfer and rejects missing offset, reversed
weights, compressed scale, wrong timing, and zero-output behavior.
