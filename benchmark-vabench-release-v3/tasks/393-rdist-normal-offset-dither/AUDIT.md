# Audit: Rdist Normal Offset Dither

- Task id: `v3_393_rdist_normal_offset_dither`
- Category: `veriloga_random_distribution_semantics`
- Required syntax focus: `Use $rdist_normal() for clocked seeded offset dither without hard-coded draw values.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior checker repaired to avoid simulator-private RNG sequence pinning.
