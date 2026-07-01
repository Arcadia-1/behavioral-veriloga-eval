# Two-Gate Audit: Task 087 LFSR PRBS Generator

## Gate 1: Admission

- Label: `independent_l1_ready` after repair.
- Human-confirmed judgment: an LFSR PRBS source is a reusable mixed-signal support/control component and can stand alone when the public prompt specifies taps, seed, enable, reset, bit order, and observable output behavior.
- Public contract: `prbs7_ref.va` implements a 7-bit PRBS source with active-low reset, enable hold behavior, public tap rule, parallel state outputs, and serial output bit.
- Artifact boundary: `task.toml`, prompt, manifests, starter, solution, and negatives now consistently target `prbs7_ref.va`; stale legacy `prbs7.va` target files were removed.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready` for the audited L1 row.
- Prompt hygiene: removed old provenance and hidden-checker wording; the public prompt now states the observable PRBS state-machine contract.
- Visible/hidden coverage: hidden coverage differs from visible by adding an enable-low hold window and longer PRBS observation; decks are not byte-identical.
- Checker strength: the checker reconstructs edge-by-edge PRBS recurrence, reset behavior, enable hold, unique-code coverage, state bit order, and serial-output bit behavior. It no longer relies on a shallow scalar check.
- Negatives: 4/4 concrete variants rejected behaviorally under EVAS and as `NEGATIVE_REJECTED` under Spectre.
- EVAS evidence: hidden gold PASS in `external-evidence/v3_batch1_gold_085_089.json`; hidden negatives 4/4 behavioral rejections in `external-evidence/v3_batch1_negatives_evas.json`.
- Spectre evidence: visible gold PASS in `external-evidence/v3_batch1_spectre_visible_gold.json`; hidden gold PASS in `external-evidence/v3_batch1_spectre_hidden_gold.json`; hidden negatives 4/4 `NEGATIVE_REJECTED` in `external-evidence/v3_batch1_spectre_hidden_negatives.json`.
- AHDL lint status: Spectre read-in completed for visible, hidden, and negative decks with no recorded AHDLLINT failure in the audited result logs.

## Residual Risk

This row is digital-voltage control logic, but it remains within scope because the PRBS source is an AMS behavioral stimulus/control primitive and the public contract is voltage-domain Verilog-A.
