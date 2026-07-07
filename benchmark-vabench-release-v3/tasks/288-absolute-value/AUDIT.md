# Smooth Absolute Value Audit

- Gate 1: `independent_l1_ready`.
- Duplicate resolution: this row is distinct from `148-absolute-value` because it requires a smooth soft-rectifier transfer with a rounded zero crossing, not an exact ideal `abs()` cusp.
- Cadence/VA modeling rationale: smooth analog behavioral transfers avoid discontinuous derivatives at sensitive operating points; this row exercises that modeling style in a memoryless rectifier primitive.
- Public contract: `absolute_value(sigin, sigout)` with public `smooth = 0.05 V`; output is `V(sigin) * tanh(V(sigin) / smooth)`.
- Checker alignment: checker evaluates the smooth even transfer over positive, negative, and near-zero input regions.
- Validation status: fresh local EVAS2 gold/negative, Spectre visible/hidden gold, Spectre hidden negative, and EVAS AHDL-like preflight validation completed after this rewrite. Generated evidence reports are intentionally not committed.
