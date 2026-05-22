# Pipeline ADC chain

- Entry: `vbr1_l2_pipeline_adc_chain`
- Level: `L2`
- Category: `Data Converters`
- Package status: `selected_l2_target`
- Score surface: `benchmark-e2e`
- Benchmark score: `enabled`
- Materialized forms: `e2e, tb`
- Missing forms: `none`
- Certification: static `pending`; EVAS `pending`; Spectre `pending`
- Evidence: `benchmark-vabench-release-v1/reports/dual_certification.json`

This release entry is materialized in the paper-facing vaBench release package.
It is a true composed pipeline ADC flow: a 2-bit coarse stage produces a
residue, a second 2-bit backend stage quantizes that residue, and the final
4-bit output concatenates the two stage decisions.
