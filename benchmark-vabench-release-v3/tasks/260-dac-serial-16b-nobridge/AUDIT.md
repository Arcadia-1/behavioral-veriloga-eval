# DAC Serial 16b Nobridge Audit

- Function: serial SAR-DAC prefix accumulator driven by sample and SAR-ready
  clocks.
- Admission note: retained as a data-converter benchmark after prompt cleanup,
  but the public contract is the modeled prefix accumulator behavior rather
  than a complete 16-bit conversion flow.
- Prompt status: public interface, `vdd`/`vcm` parameters, falling-edge reset,
  falling-edge serial accumulation, prefix weight sequence, complete array
  normalization basis, output scaling, and modeling constraints are now stated
  without source-history or checker-internal wording.
- Coverage note: visible smoke and hidden decks are now materially distinct.
  Hidden coverage adds a second sample reset and a different ready/data
  sequence to exercise prefix accumulation and restart behavior.
- Checker note: the runner now uses a semantic serial-prefix checker that tracks
  sample falling-edge resets, SAR-ready falling-edge decisions, the modeled
  prefix weights, and the complete 16-bit CDAC normalization basis.
- Evidence: current-main EVAS2 hidden gold passed; four negative variants were
  all rejected behaviorally. Spectre `sui-direct` hidden gold passed, and the
  same four hidden negative variants were all `NEGATIVE_REJECTED`. The visible
  smoke script passed after aligning it with the non-persistent EVAS2 path used
  by release validation.
- AHDL lint/read-in triage: the Spectre hidden gold/negative result JSON
  reported no task-specific warnings or errors.
- Gate 2 status: `cadence_modeling_ready` for the audited hidden gold and
  negative slice.
