# Audit: String Config Label Select

- Task id: `v3_429_string_config_label_select`
- Category: `veriloga_string_format_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises branch-dependent `$sformat()` label selection for configuration A/B while preserving an externally checked mode-dependent voltage and metric contract.
- Duplicate boundary: distinct from `426-string-sformat-mode-tag` because this row has a public mode-dependent A/B output and metric offset contract in addition to formatted labels.
- Prompt status: uses the mandatory vaBench v3 section format and exposes both configuration branches.
- Gold status: task-form `$sformat()` with destination string in both configuration branches; unused file descriptor state removed in this review pass.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution. The formatted label is a simulator side effect and does not change the voltage-domain output contract.
- Current validation status: EVAS2/Rust gold/negative 5/5 gold pass and 25/25 negatives behavior-rejected for the S1 batch; Spectre hidden/visible gold 5/5 pass; Spectre hidden negatives 25/25 behavior-rejected; AHDL lint/preflight 10/10 pass with no diagnostics.
