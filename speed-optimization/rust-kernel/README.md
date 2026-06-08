# EVAS2 Rust Coverage Audit Notes

This directory is the compact audit surface for the EVAS2 Rust-kernel coverage
evidence carried by this PR.

It is intentionally not the full historical Rustification wiki.  Older
workstream notes and large raw JSON artifacts are excluded from this split PR so
reviewers can audit the current coverage claim without following stale links.

## Included Documents

| File | Purpose |
|---|---|
| `audits/117-rustsim-while-body-gate.md` | Explains the controlled `while` body lowering gate and the release coverage change from `355/357` to `357/357` strict RustSimProgram support. |
| `audits/118-rustsim-coverage-layering-and-pulse-breakpoint.md` | Explains why Rust coverage is reported in layers and records the pulse-source breakpoint fix that prevents repeated current-time breakpoints. |
| `../reports/current_release_rust_coverage_manifest_rustsim_gate_20260606.md` | Markdown summary of the pre-while coverage manifest. |
| `../reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.md` | Markdown summary of the post-while coverage manifest. |
| `../reports/evas2_while_cppll_smoke_20260606.md` | Targeted CPPLL smoke evidence for the while-body gate. |

## Review Boundary

Use this PR to audit the coverage story only:

- which semantic layer is being counted,
- what the RustSimProgram static gate can represent,
- what was fixed in the pulse breakpoint scheduler,
- why these documents are not a Spectre AX speed claim.

Do not use these notes as a standalone speed or precision result.  The
four-simulator result table lives in the separate four-way reference PR, and the
runner/checker behavior lives in the runner/equivalence PR.

## Claim Rules

Allowed from these notes:

- The release gold model lowering gate reached `357/357` strict RustSimProgram
  support in the documented coverage artifact.
- The coverage estimate is a compile/lowering and runtime-accounting aid, not a
  measured EVAS-vs-Spectre speedup.
- The pulse breakpoint fix is a general future-breakpoint scheduling correction,
  not a benchmark-specific exception.

Not allowed from these notes alone:

- Rust EVAS2 is faster than Spectre AX.
- Rust EVAS2 is more accurate than Spectre AX.
- EVAS2 fully implements all Verilog-A semantics.
- Markdown coverage summaries are a substitute for rerunning the four-way
  experiment after simulator, checker, or benchmark changes.
