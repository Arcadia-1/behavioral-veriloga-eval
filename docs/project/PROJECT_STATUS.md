# Project Status

Last updated: 2026-05-13

## 1) Project Goal

Build two durable vaEVAS assets:

1. `vaBench`, a behavioral Verilog-A benchmark with prompts, metadata, checkers,
   gold implementations, and EVAS/Spectre validation evidence.
2. `EVAS`, a fast and debuggable evaluator aligned with Spectre on the
   benchmark-supported pure voltage-domain behavioral subset.

Controller policies, compile skills, RAG, token optimization, and local model
fine-tuning are support harnesses only. They are not the main research direction
unless the project scope is explicitly reopened.

## 2) Current Benchmark Scope

Tracked source tree:

- `tasks/`: 92 gold-backed tasks.
- Families:
  - `end-to-end`: 55
  - `spec-to-va`: 18
  - `bugfix`: 8
  - `tb-generation`: 11
- Every tracked task has `prompt.md`, `meta.json`, `checks.yaml`, and `gold/`.

Mainline local result evidence:

- `results/vabench-main-v1-main120-gold-evas-2026-05-08/summary.json`: 120/120 PASS.
- `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/summary.json`: 120/120 PASS.
- The matching `benchmark-vabench-main-v1/` source directory is not present in
  this worktree; treat `vabench-main-v1-main120` as local evidence until that
  source split is restored or materialized.

## 3) Current Snapshot (Tracked Summary)

Current mainline docs:

- `docs/VAEVAS_MAINLINE_PLAN.md`: ordered roadmap.
- `docs/VABENCH_MAIN_INVENTORY.md`: current tracked inventory and main120 evidence split.
- `docs/VAEVAS_VALIDATION_PIPELINE.md`: validation gates and commands.
- `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md`: first conformance regression targets.

Current parity facts:

- Gold main120 evidence passes both EVAS and Spectre: 120/120 each.
- Historical D old strict candidate parity had 3 EVAS PASS / Spectre FAIL false positives.
- D v2preflight reduced this to 1 false positive.
- D parityfix splice evidence has 0 binary pass/fail mismatches.

Older `A/B/C/D/E/F` workflow and repair-condition docs remain useful as
historical baseline evidence, but they are no longer the default next
investment.

## 4) Where To Look First (5-Minute Onboarding)

1. `docs/VAEVAS_MAINLINE_PLAN.md` - current strategy and work order.
2. `docs/VABENCH_MAIN_INVENTORY.md` - current benchmark inventory and gaps.
3. `docs/VAEVAS_VALIDATION_PIPELINE.md` - commands for static checks, EVAS, Spectre, and reporting.
4. `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md` - atomic parity regression backlog.
5. `AGENTS.md` - agent behavior constraints for this repo.
6. `tables/` - tracked compact result summaries.
7. `docs/EXPERIMENT_ASSET_POLICY.md` - what to keep or leave local after runs.

## 5) Storage and Versioning Policy (Current)

- Raw heavy artifacts remain local under `results/` (ignored by git).
- Tracked conclusions are stored under `tables/`.
- Source-of-truth code and benchmark definitions:
  - `tasks/`, `runners/`, `scripts/`, `schemas/`, `tests/`.

## 6) Next Execution Plan

1. Decide how to restore or materialize the 120-task `vabench-main-v1-main120`
   source split, or rebuild the paper-facing split from tracked `tasks/` plus
   expansion batches.
2. Convert the three confirmed EVAS PASS / Spectre FAIL historical causes into
   atomic conformance regressions.
3. Keep full `vaBench-main` as the broad EVAS/Spectre parity gate.
4. Expand benchmark coverage in validated batches toward roughly 200
   paper-facing tasks.
5. Run minimal model baselines only after benchmark coverage and EVAS/Spectre
   parity evidence are stable.
