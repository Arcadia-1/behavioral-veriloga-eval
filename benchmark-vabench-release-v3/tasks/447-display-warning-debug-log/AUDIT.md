# Audit: Display Warning Debug Log

- Task id: `v3_447_display_warning_debug_log`
- Category: `veriloga_system_output_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises `$display`, `$warning`, `$debug`, and an unreachable `$error` branch on a sampled voltage-domain update path.
- Duplicate boundary: distinct from `428-string-mode-tagged-log`, which uses `$strobe`; this row covers immediate simulator output calls and warning/debug syntax.
- Prompt status: updated to the mandatory vaBench v3 section format and now states that console/log output is a side effect, not a voltage-domain circuit function.
- Gold status: calls `$display`, `$warning`, and `$debug` on non-reset samples; the `$error` call is guarded by an unreachable negative-count branch to keep normal simulations non-terminating.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution. Console/log output is a simulator side effect and does not change the voltage-domain output contract.
- Current validation status: EVAS2/Rust gold/negative 5/5 gold pass and 25/25 negatives behavior-rejected for the S1 batch; Spectre hidden/visible gold 5/5 pass; Spectre hidden negatives 25/25 behavior-rejected; AHDL lint/preflight 10/10 pass with no diagnostics.
