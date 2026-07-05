# Audit: String Mode Tagged Log

- Task id: `v3_428_string_mode_tagged_log`
- Category: `veriloga_string_format_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises task-form `$sformat()` plus `$strobe()` logging while preserving the sampled voltage-domain output contract.
- Duplicate boundary: distinct from `426-string-sformat-mode-tag`, which keeps the formatted string internal and does not emit a strobe log.
- Prompt status: uses the mandatory vaBench v3 section format and makes the strobe side-effect boundary explicit.
- Gold status: task-form `$sformat()` with destination string, followed by `$strobe("%s", label_q)`; unused file descriptor state removed in this review pass.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution. The formatted string and strobe output are simulator side effects and do not change the voltage-domain output contract.
- Current validation status: EVAS2/Rust gold/negative 5/5 gold pass and 25/25 negatives behavior-rejected for the S1 batch; Spectre hidden/visible gold 5/5 pass; Spectre hidden negatives 25/25 behavior-rejected; AHDL lint/preflight 10/10 pass with no diagnostics.
