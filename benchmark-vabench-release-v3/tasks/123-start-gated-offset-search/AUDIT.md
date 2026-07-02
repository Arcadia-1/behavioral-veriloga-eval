# Audit: 123 Start Gated Offset Search

Gate 1: `independent_l1_ready`. This is a standalone comparator-offset
calibration search driver: it gates the calibration interval, interprets
comparator decisions, adapts the search step on sign changes, and drives a
differential stimulus pair around a public common mode. Human review confirmed
that converter calibration/search primitives with a reusable public contract
should count as independent data-converter benchmark components.

Gate 2: `cadence_modeling_ready` for the independent calibration-driver role.
The public prompt states the start gate, falling-clock update rule,
comparator-decision
interpretation, sign-change step halving, reset behavior, common-mode behavior,
and voltage-only constraints. Current PR validation: EVAS gold PASS, Spectre AX
hidden gold PASS, and EVAS/Spectre negatives rejected with no Spectre errors.
Spectre emitted only environment/setup warnings.

Hidden/visible coverage: repaired in this PR. The hidden deck now uses a
different comparator decision sequence from the visible smoke deck while
preserving the same public start-gated search contract.

Checker coverage: `v3_start_gated_offset_search` checks the public differential
sequence and common-mode behavior, including start gating and step halving on
decision sign changes.
