# Ready-Triggered 7-bit Capacitive DAC Audit

- Function: ready-triggered 7-bit single-ended capacitive DAC with a first-edge
  arm state and one fixed non-switching unit capacitance in the normalization.
- Admission note: retained as a distinct ready-gated CDAC behavior; smaller
  width-only variants should not receive separate counted credit without a
  stronger circuit role.
- Prompt status: public interface, thresholds, ready-edge behavior, switched
  weights, fixed unit capacitance, endpoint effect, and modeling constraints are
  now stated without source-history or checker-internal wording.
- Coverage note: visible smoke and hidden decks are now materially distinct.
  Hidden coverage changes the ready cadence and data sequence, and makes the
  first ready edge see nonzero inputs to prove the arm-before-update contract.
- Checker note: the runner now uses a semantic ready-edge checker that samples
  traced input bits at rising ready crossings, verifies the first-edge arm
  state, and recomputes the fixed-unit CDAC normalization.
- Evidence: current-main EVAS2 hidden gold passed; four negative variants were
  all rejected behaviorally. Spectre `sui-direct` hidden gold passed, and the
  same four hidden negative variants were all `NEGATIVE_REJECTED`. The visible
  smoke script passed after aligning it with the non-persistent EVAS2 path used
  by release validation.
- AHDL lint/read-in triage: the Spectre hidden gold/negative result JSON
  reported no task-specific warnings or errors.
- Gate 2 status: `cadence_modeling_ready` for the audited hidden gold and
  negative slice.
