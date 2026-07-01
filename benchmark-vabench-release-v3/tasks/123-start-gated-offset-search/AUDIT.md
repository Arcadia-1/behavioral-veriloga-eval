# Audit: 123 Start Gated Offset Search

Gate 1: `l2_support_component`. This is useful as a comparator-offset
calibration stimulus block inside a converter/calibration flow, but it is not
counted as a standalone converter function by itself.

Gate 2: `cadence_modeling_ready` for the support-component role. The public
prompt states the start gate, falling-clock update rule, comparator-decision
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
