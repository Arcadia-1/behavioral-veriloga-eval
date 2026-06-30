# Two-Gate Audit: Task 106 Programmable Stimulus Sequencer

## Gate 1: Admission

- Label: `independent_l1_ready` after repair.
- Human-confirmed judgment: a single programmable sequencer DUT is L1, not L2. It is an independent source/control component because it implements mode sequencing, ramp, chirp, and gate behavior in one reusable Verilog-A block.
- Public contract: `programmable_stimulus_sequencer.va` generates sequenced analog stimulus and metric outputs with transition-smoothed state changes.
- Artifact boundary: `task.toml` now classifies the row as L1 and targets only `programmable_stimulus_sequencer.va`; prompt, manifests, starter, solution, and negatives agree.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready` for the audited L1 row.
- Prompt hygiene: removed stale testbench/Spectre-deck wording so the prompt asks for the DUT module, not construction of a simulator testbench.
- Modeling repair: solution output contributions now use the public transition smoothing parameter instead of abrupt contributions.
- Visible/hidden coverage: visible and hidden decks are distinct and exercise different sequencer timing coverage.
- Checker strength: the streaming checker validates ramp monotonicity, chirp segment behavior, mode-switch continuity, and gate dependence. It rejects zero, flat-ramp, non-chirping, and gate-ignored variants.
- Negatives: 4/4 concrete variants rejected behaviorally under EVAS and as `NEGATIVE_REJECTED` under Spectre.
- EVAS evidence: hidden gold PASS in `external-evidence/v3_batch1_gold_106.json`; hidden negatives 4/4 behavioral rejections in `external-evidence/v3_batch1_negatives_evas.json`.
- Spectre evidence: visible gold PASS in `external-evidence/v3_batch1_spectre_visible_gold.json`; hidden gold PASS in `external-evidence/v3_batch1_spectre_hidden_gold.json`; hidden negatives 4/4 `NEGATIVE_REJECTED` in `external-evidence/v3_batch1_spectre_hidden_negatives.json`.
- AHDL lint status: Spectre read-in completed for visible, hidden, and negative decks with no recorded AHDLLINT failure in the audited result logs.

## Residual Risk

No local blocker remains after the current L1 reclassification and checker/negative repair. It should not be described as L2 unless rewritten into a composed measurement or subsystem flow.
