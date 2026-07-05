# Audit: String Swrite Label Builder

- Task id: `v3_425_string_swrite_label_builder`
- Category: `veriloga_string_format_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises `$swrite()` as an internal string side effect on the same sampled update path as voltage-domain outputs.
- Duplicate boundary: distinct from `427-string-formatted-metric-line`, which emits the formatted string through file I/O.
- Prompt status: updated to the mandatory vaBench v3 section format and no longer uses the old free-form `Interface` scaffold.
- Gold status: removes unused file descriptor state, keeps `$swrite()` internal-only, and formats explicit count/metric/mode fields.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- EVAS2/Rust evidence: fresh strict full-model validation passes gold and rejects all five negative variants behaviorally after string side-effect support.
- Spectre evidence: visible and hidden gold validation pass; hidden Spectre negative validation rejects all five negative variants.
- AHDL/lint status: EVAS AHDL-like lint preflight passes visible and hidden cases with zero diagnostics. Spectre runs complete with 0 errors; the remaining `VACOMP-2435` read-in warning is the shared `CDS_AHDLCMI_ENABLE` environment warning, not task-specific Verilog-A modeling debt.
