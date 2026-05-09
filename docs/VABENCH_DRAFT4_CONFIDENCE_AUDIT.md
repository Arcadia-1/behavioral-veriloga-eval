# vaBench-main-v1 Draft4 Confidence Audit

**Date**: 2026-05-08

This document records the benchmark review loop run before continuing expansion
beyond draft4.  The goal is not mathematical certainty; it is factual confidence
under explicit, repeatable gates that target the main ways a benchmark can look
healthy while still being invalid.

## Initial Concern

The draft4 benchmark had already passed strict-EVAS and Spectre, but simulator
success alone does not prove benchmark integrity.  In particular, a benchmark can
still be flawed if it:

- routes checkers through historical task ids or source registries;
- exposes checker/gold internals in public prompts;
- misses one of the four required task forms per pack;
- accidentally includes heldout packs in main;
- has prompt/checker/gold contract drift;
- reports old results after changing checker semantics.

## Audit Loop

| Iteration | Finding | Fix | Verification |
| --- | --- | --- | --- |
| 1 | Semantic audit had 5 WARNs from `checker_source_task_not_named`; this meant old seed checkers still delegated to historical source task ids. | Replaced strongarm and PFD checkers with benchmark-local public CSV behavior checks. | Semantic audit became `16 PASS / 0 WARN / 0 FAIL`. |
| 2 | There was no hard benchmark-integrity gate for hidden source routing, heldout contamination, or pack-form completeness. | Added `runners/audit_vabench_benchmark_integrity.py`. | Integrity audit returned `PASS`, `issue_counts={}`. |
| 3 | Checker semantics changed, so old EVAS/Spectre 16/16 results could not be reused. | Reran gold validation under the public-checker benchmark. | strict-EVAS `16/16`; Spectre `16/16`. |

## Current Gate Results

| Gate | Result | Artifact |
| --- | --- | --- |
| Semantic prompt/checker/gold audit | `16 PASS / 0 WARN / 0 FAIL` | `analysis/vabench-main-v1_semantic_contract_audit_20260508.json` |
| Benchmark integrity audit | `PASS`, no issues | `analysis/vabench-main-v1_integrity_audit_20260508.json` |
| Gold strict-EVAS | `16/16 PASS` | `results/vabench-main-v1-draft4-publiccheckers-gold-evas-2026-05-08/summary.json` |
| Gold Spectre | `16/16 PASS` | `results/vabench-main-v1-draft4-publiccheckers-gold-spectre-jin-2026-05-08/summary.json` |

## Remaining Non-Zero Risks

No benchmark strategy deserves literal 100% confidence.  The remaining risks are
now explicit and bounded:

| Risk | Why it remains | Mitigation before full benchmark freeze |
| --- | --- | --- |
| Checker permissiveness | A public checker can pass a behavior that is too broad. | Add adversarial negative tests for each checker family. |
| Functional diversity | Draft4 is still threshold-heavy: 3 threshold/static packs plus 1 event/timing pack. | Next expansion batch must add memory, timing, and data-conversion packs before model runs. |
| Runtime skew | PFD dense waveform dominates validation time. | Add runtime accounting and consider shorter equivalent public harnesses where behavior is preserved. |
| Manual prompt quality | Heuristic audits cannot prove prompts are ideal. | Human review plus model smoke before declaring benchmark freeze. |
| Full-scale representativeness | 4/30 packs is an audited draft, not the final main benchmark. | Continue batch expansion with the same gates. |

## Verdict

For the current 4-pack / 16-task draft, I have factual confidence that it is
suitable to continue benchmark expansion:

- no known hidden source-task checker routing remains;
- no semantic audit warnings remain;
- no benchmark-integrity audit issues remain;
- gold artifacts pass both strict-EVAS and real Spectre under the maintained
  `jin` bridge profile.

The benchmark is not yet large or diverse enough for final model comparison.
The next work should expand non-threshold families under the same audit loop,
not run the main A/D/C/S matrix yet.
