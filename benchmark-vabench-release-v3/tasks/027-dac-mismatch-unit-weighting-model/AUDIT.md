# Audit: 027 DAC Mismatch Unit Weighting Model

Gate 1: `independent_l1_ready`. This is a 4-bit DAC transfer model with
explicit nonideal unit weights. It is independent from the canonical binary
DAC because the public behavior is a mismatch-weighted reconstruction rather
than ideal powers-of-two weighting.

Gate 2: `cadence_modeling_ready`. The public prompt states the interface,
nonideal weights, all-active normalization rule, endpoints, transition
smoothing, and voltage-only constraints without exposing a precomputed total
weight. Current PR validation: EVAS gold PASS, Spectre AX hidden gold PASS,
and EVAS/Spectre negatives rejected with no Spectre errors. Spectre emitted
only environment/setup warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck checks low-code, mid-code, and full-scale mismatch-weighted
levels.

Checker coverage: `v3_027_dac_mismatch_unit_weighting_model` enforces the
public mismatch-weighted transfer function and rejects wrong gain, idealized or
swapped weights, missing units, saturation, and endpoint mistakes.
