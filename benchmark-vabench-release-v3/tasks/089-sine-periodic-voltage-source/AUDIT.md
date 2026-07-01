# Two-Gate Audit: Task 089 Sine Periodic Voltage Source

## Gate 1: Admission

- Label: `independent_l1_ready` after repair.
- Human-confirmed judgment: this row is acceptable as a standalone reusable voltage-source primitive because the prompt and checker now evaluate a concrete multi-tone waveform, not just a generic testbench source placeholder.
- Public contract: `multitone.va` generates a periodic analog voltage source with three sinusoidal tone components, public amplitude/frequency/phase-style parameters, and transition-smoothed output.
- Artifact boundary: `task.toml`, prompt, manifests, starter, solution, and negatives agree on `multitone.va`.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready` for the audited L1 row.
- Prompt hygiene: removed hidden-evaluator/provenance wording and kept the public contract at the observable waveform level.
- Visible/hidden coverage: visible and hidden decks use distinct stop/stimulus coverage and are not byte-identical.
- Checker strength: the checker samples the waveform against the public three-tone formula and checks mean/max error plus waveform span, rejecting zero, missing-tone, wrong-frequency, and half-amplitude variants.
- Negatives: 4/4 concrete variants rejected behaviorally under EVAS and as `NEGATIVE_REJECTED` under Spectre.
- EVAS evidence: hidden gold PASS in `external-evidence/v3_batch1_gold_085_089.json`; hidden negatives 4/4 behavioral rejections in `external-evidence/v3_batch1_negatives_evas.json`.
- Spectre evidence: visible gold PASS in `external-evidence/v3_batch1_spectre_visible_gold.json`; hidden gold PASS in `external-evidence/v3_batch1_spectre_hidden_gold.json`; hidden negatives 4/4 `NEGATIVE_REJECTED` in `external-evidence/v3_batch1_spectre_hidden_negatives.json`.
- AHDL lint status: Spectre read-in completed for visible, hidden, and negative decks with no recorded AHDLLINT failure in the audited result logs.

## Residual Risk

The row remains a source primitive rather than a complete application circuit. It is valid as L1 source-function coverage under the current benchmark policy.
