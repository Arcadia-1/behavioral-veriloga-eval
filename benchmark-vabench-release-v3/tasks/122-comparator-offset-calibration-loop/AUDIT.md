# Two-Gate SOP Audit: Task 122 Comparator Offset Calibration Loop

## Scope

Task 122 is rewritten from a duplicate offset-search helper into a comparator
offset calibration loop. The target module drives a supplied comparator with a
successive-approximation differential stimulus, reads the comparator decision,
and reports the signed offset estimate plus a valid flag.

## Gate 1: Admission And Counting

- Admission label: `l2_measurement_ready`.
- Function boundary: closed-loop comparator offset calibration, not just an
  open-loop offset stimulus driver.
- Independence rationale: unlike `203-comparator-offset-driver` and
  `208-offset-bisection-driver`, this row evaluates convergence against a
  supplied comparator and requires an offset estimate/valid reporting path.
- Counting status: replacement candidate; final counted status and row-number
  policy need human/upstream confirmation.

## Gate 2: Cadence Modeling Quality

- Cadence correspondence: maps to comparator offset measurement/calibration
  examples in the Verilog-A reference material, where a measurement component
  observes a DUT and reports an offset metric after a controlled stimulus flow.
- Prompt hygiene: public prompt separates target DUT from supplied support
  comparator and avoids support offset values or checker thresholds.
- Checker coverage: `v3_comparator_offset_calibration_loop` checks final
  estimate/reference agreement, generated differential symmetry, estimate
  output consistency, update count, and valid assertion.
- Evidence status: EVAS visible smoke passes; EVAS gold/negative verification
  passes with 1 gold accepted and 5 behavioral negatives rejected. Spectre
  hidden and visible gold pass. Spectre hidden negative audit rejects all 5
  negatives as behavioral failures. AHDL warning triage found no task-specific
  transition warning after the transition-input repair; only environment-level
  Spectre warnings remain.

## Review Note

This row replaces a duplicate offset-search helper. It should remain L2 only if
the reviewer accepts closed-loop calibration plus estimate reporting as distinct
from the retained offset-driver L1 rows.
