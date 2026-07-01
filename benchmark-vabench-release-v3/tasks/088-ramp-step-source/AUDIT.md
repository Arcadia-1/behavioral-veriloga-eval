# Two-Gate Audit: Task 088 Ramp Step Source

## Gate 1: Admission

- Label: `independent_l1_ready` after repair.
- Human-confirmed judgment: a periodic bounded ramp/step source with a guard output is a reusable source component, not merely a simulator syntax row, when the checker evaluates the ramp and guard behavior.
- Public contract: `bound_step_period_guard_ref.va` emits a repeating bounded ramp-like source and a guard indicator with public period, transition, and guard-window semantics.
- Artifact boundary: `task.toml`, prompt, manifests, starter, solution, and negatives agree on `bound_step_period_guard_ref.va`.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready` for the audited L1 row.
- Prompt hygiene: removed migration/private-checker wording and kept the prompt focused on the source behavior.
- Visible/hidden coverage: visible and hidden decks differ in timing/stop coverage and are not byte-identical.
- Checker strength: the checker verifies ramp/guard span, repeated wraps, period consistency, non-wrap phase monotonicity, guard high fraction, and guard/phase alignment, rejecting zero, no-wrap, always-low guard, and wrong guard-width variants.
- Negatives: 4/4 concrete variants rejected behaviorally under EVAS and as `NEGATIVE_REJECTED` under Spectre.
- EVAS evidence: hidden gold PASS in `external-evidence/v3_batch1_gold_085_089.json`; hidden negatives 4/4 behavioral rejections in `external-evidence/v3_batch1_negatives_evas.json`.
- Spectre evidence: visible gold PASS in `external-evidence/v3_batch1_spectre_visible_gold.json`; hidden gold PASS in `external-evidence/v3_batch1_spectre_hidden_gold.json`; hidden negatives 4/4 `NEGATIVE_REJECTED` in `external-evidence/v3_batch1_spectre_hidden_negatives.json`.
- AHDL lint status: Spectre read-in completed for visible, hidden, and negative decks with no recorded AHDLLINT failure in the audited result logs.

## Residual Risk

No local blocker remains after current review. The row should still be counted under the global source-component policy rather than as a composed L2 flow.
