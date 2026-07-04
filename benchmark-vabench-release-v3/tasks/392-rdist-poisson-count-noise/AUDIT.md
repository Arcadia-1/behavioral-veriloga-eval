# Audit: Rdist Poisson Count Noise

- Task id: `v3_392_rdist_poisson_count_noise`
- Category: `veriloga_random_distribution_semantics`
- Required syntax focus: `Use $rdist_poisson() for clocked seeded count-like variation without hard-coded draw values.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior checker repaired to avoid simulator-private RNG sequence pinning.
