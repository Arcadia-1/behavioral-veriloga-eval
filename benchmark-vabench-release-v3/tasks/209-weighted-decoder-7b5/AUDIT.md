# Weighted Decoder 7b5 Audit

- Function: voltage-coded bipolar SAR decision decoder producing 7-bit,
  7.5-bit, and 8-bit reconstructed analog outputs from one decision vector.
- Admission note: retained as the representative redundant SAR / paired-LSB
  decoder for this review group; same-function rows should not receive separate
  counted credit unless rewritten with a distinct circuit role.
- Prompt status: public interface, threshold parameter, weighting ladder,
  paired-LSB behavior, fixed-unit normalization basis, and modeling constraints
  are now stated without source-history or checker-internal wording.
- Coverage note: visible smoke and hidden decks are now materially distinct.
  Hidden coverage uses a separate five-code decision sequence and exercises the
  redundant weight-8 term, half-bit refinement, and paired-LSB ternary behavior.
- Checker note: the runner now uses a semantic weighted-reconstruction checker
  instead of fixed sample tables. It recomputes the shared redundant SAR basis,
  paired-LSB output, and common normalization from traced decision bits.
- Evidence: current-main EVAS2 hidden gold passed; four negative variants were
  all rejected behaviorally. Spectre `sui-direct` hidden gold passed, and the
  same four hidden negative variants were all `NEGATIVE_REJECTED`. The visible
  smoke script passed after aligning it with the non-persistent EVAS2 path used
  by release validation.
- AHDL lint/read-in triage: the Spectre hidden gold/negative result JSON
  reported no task-specific warnings or errors.
- Gate 2 status: `cadence_modeling_ready` for the audited hidden gold and
  negative slice.
