# Audit: Rtoi Conversion Quantizer

- Task id: `v3_484_rtoi_conversion_quantizer`
- Category: `veriloga_conversion_semantics`
- Scope: Verilog-A semantic/support row for `$rtoi()` in a voltage-domain quantizer.
- Public behavior: `$rtoi(8.0 * V(in))` is clamped to code range 0 through 7 and normalized onto `out`.
- Review note: the conversion helper is part of the public contract; a threshold-only replacement is outside the task.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. Spectre reports only the shared `VACOMP-2435` environment notice.
