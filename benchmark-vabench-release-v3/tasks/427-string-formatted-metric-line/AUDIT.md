# Audit: String Formatted Metric Line

- Task id: `v3_427_string_formatted_metric_line`
- Category: `veriloga_string_format_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises `$swrite()` plus `$fopen`/`$fwrite`/`$fclose` append-style file emission while preserving the same voltage-domain output contract.
- Duplicate boundary: distinct from `425-string-swrite-label-builder`, which keeps the formatted string internal and does not perform file I/O.
- Prompt status: updated to the mandatory vaBench v3 section format and made the file side-effect boundary explicit.
- Gold status: cleans the formatted/write block, formats explicit count/metric/mode fields, and appends each metric line to avoid repeated file-overwrite warnings.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- EVAS2/Rust evidence: fresh strict full-model validation passes gold and rejects all five negative variants behaviorally after string/file side-effect support.
- Spectre evidence: visible and hidden gold validation pass; hidden Spectre negative validation rejects all five negative variants. The file is opened in append mode so repeated sampled writes do not trigger file-overwrite behavior.
- AHDL/lint status: EVAS AHDL-like lint preflight passes visible and hidden cases with zero diagnostics. Spectre runs complete with 0 errors; the remaining `VACOMP-2435` read-in warning is the shared `CDS_AHDLCMI_ENABLE` environment warning, not task-specific Verilog-A modeling debt.
