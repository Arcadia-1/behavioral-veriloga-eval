# Audit: Fstrobe File Line Writer

- Task id: `v3_446_fstrobe_file_line_writer`
- Category: `veriloga_system_output_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises `$fopen`/`$fstrobe`/`$fclose` file-output syntax on a sampled voltage-domain update path.
- Duplicate boundary: distinct from `427-string-formatted-metric-line`, which formats a string with `$swrite()` before file emission; this row directly exercises `$fstrobe()` line emission.
- Prompt status: updated to the mandatory vaBench v3 section format and now states that file output is a side effect, not a voltage-domain circuit function.
- Gold status: opens `fstrobe_lines.log` once at `initial_step`, writes sampled count/output lines with `$fstrobe`, and closes the handle at `final_step`.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution. The file write is a simulator side effect and does not change the voltage-domain output contract.
- Current validation status: EVAS2/Rust gold/negative 5/5 gold pass and 25/25 negatives behavior-rejected for the S1 batch; Spectre hidden/visible gold 5/5 pass; Spectre hidden negatives 25/25 behavior-rejected; AHDL lint/preflight 10/10 pass with no diagnostics.
