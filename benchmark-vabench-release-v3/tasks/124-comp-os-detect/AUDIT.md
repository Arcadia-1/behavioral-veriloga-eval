# Audit: 124 Comparator Offset Detect

Gate 1: `l2_support_component`. This is useful as a comparator-offset
calibration support block, but it is not counted as a standalone converter
function by itself.

Gate 2: `cadence_modeling_ready` for the support-component role. The public
prompt states the falling-clock decision rule, detector polarity, step halving
after every decision, differential output behavior, common-mode behavior, and
voltage-only constraints. Current PR validation: EVAS gold PASS, Spectre AX
hidden gold PASS, and EVAS/Spectre negatives rejected with no Spectre errors.
Spectre emitted only environment/setup warnings.

Hidden/visible coverage: repaired in this PR. The hidden deck now uses a
different detector decision sequence from the visible smoke deck while
preserving the same public offset-detect contract.

Checker coverage: `v3_comp_os_detect` checks the public differential sequence
and common-mode behavior, including polarity and per-decision step halving.
