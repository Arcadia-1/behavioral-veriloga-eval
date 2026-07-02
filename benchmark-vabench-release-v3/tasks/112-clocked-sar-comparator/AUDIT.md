# Audit: 112-clocked-sar-comparator

## Gate 1

- Label: `independent_l1_ready`.
- Function: SAR comparator primitive with clock-low precharge-high behavior and
  differential rising-edge decisions.
- Independence: retained as distinct from reset-low comparator variants because
  the precharge-high/equal-input behavior is a different converter front-end
  primitive, not just a parameter value.
- Interface role: human review treats this analog-to-decision boundary as a
  meaningful data-converter benchmark candidate, not a disposable support-only
  helper. Upstream can still decide whether to count it in the main L1 set or
  in a converter-interface subcategory.
- Duplicate policy: `116-clocked-comparator-reset-low` is treated as the
  non-counted reset-polarity variant in this review batch.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: removed source-provenance and hidden-evaluator wording.
- Public contract now exposes module/ports, `vdd`, `td_cmp`, `tr`, clock edge
  behavior, equal-input behavior, and voltage-domain constraints.
- Visible/hidden relationship: hidden testbench is no longer byte-identical to
  visible smoke; hidden coverage adds an equal-input rising-edge decision and a
  later reset window.
- Checker: `v3_clocked_sar_comparator`, stable-window samples for positive,
  negative, equal-input, and reset-precharge states.
- Functional sanity vectors:
  - `VINP > VINN` after rising clock: `DCMPP=0.9`, `DCMPN=0`.
  - `VINP < VINN` after rising clock: `DCMPP=0`, `DCMPN=0.9`.
  - `VINP == VINN` after rising clock: both decision outputs low.
  - Clock falling reset/precharge: both decision outputs high.
- Cadence reference correspondence: Cadence Verilog-AMS interface-element and
  comparator examples publish thresholds, output levels, initial state, event
  timing, and transition behavior at analog/digital boundaries. This row adapts
  that mixed-signal boundary pattern into pure voltage-domain Verilog-A outputs
  so it remains reviewable in the current v3 surface.

## Validation

- EVAS hidden gold: PASS.
- EVAS negative variants: 4/4 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: 4/4 rejected.
- AHDL lint triage: no `AHDLLINT-*` findings. Spectre reported only
  `VACOMP-2435` and `SPECTRE-592` environment/mode warnings.
