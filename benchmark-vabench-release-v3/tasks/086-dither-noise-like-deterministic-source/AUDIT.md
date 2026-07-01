# Two-Gate Audit: Task 086 Dither Noise-Like Deterministic Source

## Gate 1: Admission

- Label: `independent_l1_ready` after repair.
- Human-confirmed judgment: this is a standalone source/shaping component, distinct from the larger gain-extraction flow, if the task evaluates deterministic sampled dither injection rather than a generic testbench sine source.
- Public contract: `noise_gen_ref.va` adds a bounded, zero-mean, sampled pseudo-noise-like dither component to the input and drives the output through `transition()`.
- Artifact boundary: `task.toml`, prompt, manifests, starter, solution, and negatives now consistently target `noise_gen_ref.va`; stale legacy `noise_gen.va` target files were removed.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready` for the audited L1 row.
- Modeling repair: the previous one-shot/random-style behavior was replaced with a deterministic periodic sampled pseudo-noise sequence using a public timer-update contract, avoiding EVAS/Spectre random and one-shot timer ambiguity.
- Prompt hygiene: removed hidden-evaluator/source-provenance text and exposed the observable dither contract without leaking hidden sample windows.
- Visible/hidden coverage: visible and hidden decks use different input timing/stop windows and are not byte-identical.
- Checker strength: the checker verifies nonzero bounded dither, near-zero mean, expected statistical scale range, and amplitude bounds, rejecting passthrough, zero, excessive, and biased dither variants.
- Negatives: 4/4 concrete variants rejected behaviorally under EVAS and as `NEGATIVE_REJECTED` under Spectre.
- EVAS evidence: hidden gold PASS in `external-evidence/v3_batch1_gold_085_089.json`; hidden negatives 4/4 behavioral rejections in `external-evidence/v3_batch1_negatives_evas.json`.
- Spectre evidence: visible gold PASS in `external-evidence/v3_batch1_spectre_visible_gold.json`; hidden gold PASS in `external-evidence/v3_batch1_spectre_hidden_gold.json`; hidden negatives 4/4 `NEGATIVE_REJECTED` in `external-evidence/v3_batch1_spectre_hidden_negatives.json`.
- AHDL lint status: Spectre read-in completed for visible, hidden, and negative decks with no recorded AHDLLINT failure in the audited result logs.

## Residual Risk

The checker validates deterministic dither statistics and bounds, not a physical noise process. That is intentional for a deterministic benchmark row and is now reflected in the prompt.
