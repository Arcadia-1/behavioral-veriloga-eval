# Two-Gate Audit: Task 085 Burst Clock Source

## Gate 1: Admission

- Label: `independent_l1_ready` after repair.
- Human-confirmed judgment: a reusable burst clock source is a legitimate standalone L1 source/control component when it has its own public behavior boundary and checker, not merely a hidden testbench artifact.
- Public contract: `clk_burst_gen.va` drives `CLK_OUT` from `CLK_IN`, emits a burst only after `RESET` deasserts, uses a public divide ratio and pass-cycle count, and holds the output low outside the burst window.
- Artifact boundary: `task.toml`, prompt, visible/hidden manifests, starter, solution, and negative variants all target `clk_burst_gen.va`.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready` for the audited L1 row.
- Prompt hygiene: removed migration/hidden-evaluator style wording; the prompt now states the public module contract rather than private checker internals.
- Visible/hidden coverage: visible is a public smoke deck; hidden uses a distinct reset/release timing and stop window. Hash comparison confirmed the visible and hidden decks are not byte-identical.
- Checker strength: the checker derives burst-cycle behavior from observed clock cycles and reset timing, so it rejects always-zero, always-pass, one-cycle-only, and wrong-divider variants behaviorally.
- Negatives: 4/4 concrete variants rejected behaviorally under EVAS and as `NEGATIVE_REJECTED` under Spectre.
- EVAS evidence: hidden gold PASS in `/private/tmp/v3_batch1_gold_085_089.json`; hidden negatives 4/4 behavioral rejections in `/private/tmp/v3_batch1_negatives_evas.json`.
- Spectre evidence: visible gold PASS in `/private/tmp/v3_batch1_spectre_visible_gold.json`; hidden gold PASS in `/private/tmp/v3_batch1_spectre_hidden_gold.json`; hidden negatives 4/4 `NEGATIVE_REJECTED` in `/private/tmp/v3_batch1_spectre_hidden_negatives.json`.
- AHDL lint status: Spectre read-in completed for visible, hidden, and negative decks with no recorded AHDLLINT failure in the audited result logs.

## Residual Risk

Release counting is still governed by the global issue #29 denominator policy, but this row no longer has a known local prompt, artifact-boundary, hidden-coverage, or negative-strength blocker.
