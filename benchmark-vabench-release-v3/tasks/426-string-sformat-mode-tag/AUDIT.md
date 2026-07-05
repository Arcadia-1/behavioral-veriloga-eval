# Audit: String Sformat Mode Tag

- Task id: `v3_426_string_sformat_mode_tag`
- Category: `veriloga_string_format_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises Spectre-compatible task-form `$sformat()` with an explicit destination string on the same sampled update path as voltage-domain outputs.
- Duplicate boundary: distinct from `425-string-swrite-label-builder` because this row exercises `$sformat()` rather than `$swrite()`; distinct from `428-string-mode-tagged-log` because this row does not emit the formatted text through `$strobe()`.
- Prompt status: uses the mandatory vaBench v3 section format and makes the string side-effect boundary explicit.
- Gold status: task-form `$sformat()` with destination string; unused file descriptor state removed in this review pass.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution. The formatted string is a simulator side effect and does not change the voltage-domain output contract.
- Current validation status: EVAS2/Rust gold/negative 5/5 gold pass and 25/25 negatives behavior-rejected for the S1 batch; Spectre hidden/visible gold 5/5 pass; Spectre hidden negatives 25/25 behavior-rejected; AHDL lint/preflight 10/10 pass with no diagnostics.
