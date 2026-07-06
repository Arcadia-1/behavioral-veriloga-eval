# Smooth Limiting Diffamp Audit

- Gate 1: `independent_l1_ready`.
- Duplicate resolution: this row is distinct from hard-clamped limiter/diffamp rows because it requires a continuous tanh soft-limiting transfer.
- Cadence/VA modeling rationale: Cadence training material explicitly uses smooth nonlinear transfer functions such as `tanh` for differential-amplifier limiting, avoiding hard derivative discontinuities.
- Public contract: `limiting_diffamp(sigin_p, sigin_n, sigout)` with public `gain = 4.0` and `limit = 0.75 V`; output is a smooth odd transfer that is approximately linear near zero and asymptotically approaches `+limit`/`-limit`.
- Checker alignment: checker evaluates low soft-limit, near-linear, and high soft-limit regions while preserving polarity.
- Validation status: fresh local EVAS2 gold/negative, Spectre visible/hidden gold, Spectre hidden negative, and EVAS AHDL-like preflight validation completed after this rewrite. Generated evidence reports are intentionally not committed.
