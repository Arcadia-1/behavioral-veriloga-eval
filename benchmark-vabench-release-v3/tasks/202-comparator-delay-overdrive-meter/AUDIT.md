# Two-Gate SOP Audit: Task 202 Comparator Delay Overdrive Meter

## Scope

Task 202 is rewritten from a duplicate reset-high clocked-comparator variant
into a comparator delay/overdrive characterization meter. The target observes a
supplied clocked comparator and reports clock-to-decision delay, sampled input
overdrive, decision polarity, and valid.

## Gate 1: Admission And Counting

- Admission label: `l2_measurement_ready`.
- Function boundary: comparator timing characterization, not another clocked
  comparator reset-polarity variant.
- Independence rationale: distinct from `041-propagation-delay-comparator`
  because the target here is the characterization meter itself and it reports
  delay together with sampled overdrive and decision polarity across multiple
  comparator decisions.
- Counting status: replacement candidate; final counted status and row-number
  policy need human/upstream confirmation.

## Gate 2: Cadence Modeling Quality

- Cadence correspondence: maps to Cadence comparator examples that use
  transition-delayed decisions and to measurement-component patterns that
  report timing/metric outputs from observed waveform events.
- Prompt hygiene: public prompt defines measured observables and target/support
  boundary without exposing the support comparator delay formula.
- Checker coverage: `v3_comparator_delay_overdrive_meter` derives expected
  delay, overdrive, polarity, and valid behavior from clock/input/output
  crossing events in the saved waveform.
- Evidence status: EVAS visible smoke passes; EVAS gold/negative verification
  passes with 1 gold accepted and 5 behavioral negatives rejected. Spectre
  hidden and visible gold pass. Spectre hidden negative audit rejects all 5
  negatives as behavioral failures. Spectre initially reported VACOMP-1116 on
  continuous expressions passed through `transition()`; the gold, support, and
  negative variants were repaired to transition discrete state and multiply by
  the rail outside the transition. Re-run output has no VACOMP-1116; only
  environment-level Spectre warnings remain.

## Review Note

This row should be reviewed as an L2 characterization helper. It is not a
replacement for the retained clocked comparator DUT rows.
