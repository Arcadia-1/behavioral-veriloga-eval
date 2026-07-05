# Audit: Rdist Uniform Seeded Dither

- Task id: `v3_448_rdist_uniform_seeded_dither`
- Category: `veriloga_random_distribution_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises seeded `$rdist_uniform()` as a sampled dither source with the random draw exposed on `metric`.
- Prompt status: updated to the mandatory vaBench v3 section format and removed task-number-specific seed constants from the public contract.
- Gold status: implementation remains a deterministic seeded uniform dither example.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- EVAS2/Rust evidence: fresh strict full-model validation passes gold and rejects all five negative variants behaviorally after seeded `$rdist_uniform()` support.
- Spectre evidence: visible and hidden gold validation pass; hidden Spectre negative validation rejects all five negative variants.
- AHDL/lint status: EVAS AHDL-like lint preflight passes visible and hidden cases with zero diagnostics. Spectre runs complete with 0 errors; the remaining `VACOMP-2435` read-in warning is the shared `CDS_AHDLCMI_ENABLE` environment warning, not task-specific Verilog-A modeling debt.
