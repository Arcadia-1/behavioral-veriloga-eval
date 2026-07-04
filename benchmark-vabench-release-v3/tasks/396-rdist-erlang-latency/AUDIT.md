# Audit: Rdist Erlang Latency

- Task id: `v3_396_rdist_erlang_latency`
- Category: `veriloga_random_distribution_semantics`
- Required syntax focus: `Use $rdist_erlang() for clocked seeded multi-stage latency variation without hard-coded draw values.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior checker repaired to avoid simulator-private RNG sequence pinning.
