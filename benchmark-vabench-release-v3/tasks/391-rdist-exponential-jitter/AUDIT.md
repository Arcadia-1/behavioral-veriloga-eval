# Audit: Rdist Exponential Jitter

- Task id: `v3_391_rdist_exponential_jitter`
- Category: `veriloga_random_distribution_semantics`
- Required syntax focus: `Use $rdist_exponential() for clocked seeded jitter modeling without hard-coded draw values.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior checker repaired to avoid simulator-private RNG sequence pinning.
