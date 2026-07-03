# Two-Gate SOP Audit: Task 124 Hysteresis Trip Characterizer

## Scope

Task 124 is rewritten from a duplicate offset-search helper into a comparator
hysteresis characterization meter. The target observes a supplied hysteretic
comparator, captures the input voltage at rising and falling output trips, and
reports the hysteresis width.

## Gate 1: Admission And Counting

- Admission label: `l2_measurement_ready`.
- Function boundary: observable hysteresis-trip measurement, not implementation
  of the hysteretic comparator itself.
- Independence rationale: distinct from `292-hysteretic-comparator-receiver`
  because this row evaluates a measurement/characterization component wrapped
  around a supplied comparator DUT.
- Counting status: replacement candidate; final counted status and row-number
  policy need human/upstream confirmation.

## Gate 2: Cadence Modeling Quality

- Cadence correspondence: maps to the Verilog-A reference rectangular
  hysteresis comparator model and the measurement-component style used for
  offset/DNL/INL characterization examples.
- Prompt hygiene: public prompt defines measured observables and target/support
  boundary without exposing support thresholds or checker tolerances.
- Checker coverage: `v3_hysteresis_trip_characterizer` derives expected trip
  voltages from saved waveform crossing events and verifies latest trip pair,
  width, and valid flag.
- Evidence status: EVAS visible smoke passes; EVAS gold/negative verification
  passes with 1 gold accepted and 5 behavioral negatives rejected. Spectre
  hidden and visible gold pass. Spectre hidden negative audit rejects all 5
  negatives as behavioral failures. A weak first-trip-only negative was replaced
  with a capture-output-voltage negative after EVAS exposed that the old
  negative was not distinguishable from the gold on the current stimulus.
  AHDL warning triage found no task-specific transition warning after the
  transition-input repair; only environment-level Spectre warnings remain.

## Review Note

This row is intended to add comparator L2 measurement coverage without adding
another comparator transfer-function DUT.
