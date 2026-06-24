# Config Gate 128b Static Enable

Implement one Verilog-A DUT file named `config_latch_128b.va`.

## Interface

Define module `config_latch_128b` with scalar electrical ports in this exact order:

```text
en, d127, d126, d125, d124, d123, d122, d121, d120, d119, d118, d117, d116, d115, d114, d113, d112, d111, d110, d109, d108, d107, d106, d105, d104, d103, d102, d101, d100, d99, d98, d97, d96, d95, d94, d93, d92, d91, d90, d89, d88, d87, d86, d85, d84, d83, d82, d81, d80, d79, d78, d77, d76, d75, d74, d73, d72, d71, d70, d69, d68, d67, d66, d65, d64, d63, d62, d61, d60, d59, d58, d57, d56, d55, d54, d53, d52, d51, d50, d49, d48, d47, d46, d45, d44, d43, d42, d41, d40, d39, d38, d37, d36, d35, d34, d33, d32, d31, d30, d29, d28, d27, d26, d25, d24, d23, d22, d21, d20, d19, d18, d17, d16, d15, d14, d13, d12, d11, d10, d9, d8, d7, d6, d5, d4, d3, d2, d1, d0, q127, q126, q125, q124, q123, q122, q121, q120, q119, q118, q117, q116, q115, q114, q113, q112, q111, q110, q109, q108, q107, q106, q105, q104, q103, q102, q101, q100, q99, q98, q97, q96, q95, q94, q93, q92, q91, q90, q89, q88, q87, q86, q85, q84, q83, q82, q81, q80, q79, q78, q77, q76, q75, q74, q73, q72, q71, q70, q69, q68, q67, q66, q65, q64, q63, q62, q61, q60, q59, q58, q57, q56, q55, q54, q53, q52, q51, q50, q49, q48, q47, q46, q45, q44, q43, q42, q41, q40, q39, q38, q37, q36, q35, q34, q33, q32, q31, q30, q29, q28, q27, q26, q25, q24, q23, q22, q21, q20, q19, q18, q17, q16, q15, q14, q13, q12, q11, q10, q9, q8, q7, q6, q5, q4, q3, q2, q1, q0
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. Treat logic inputs as 0/0.9 V using `vth`.

## Required Behavior

When `en` is high, drive each `qN` to the corresponding `dN`. When `en` is low, drive all 128 outputs low.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

## Output

Return exactly `config_latch_128b.va`. Do not generate a Spectre testbench.
