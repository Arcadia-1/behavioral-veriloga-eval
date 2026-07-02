# Audit: 112-clocked-sar-comparator

## Gate 1

- Label: `independent_l1_ready`.
- Function: SAR comparator primitive with clock-low precharge-high behavior and
  differential rising-edge decisions.
- Independence: retained as distinct from reset-low comparator variants because
  the precharge-high/equal-input behavior is a different converter front-end
  primitive, not just a parameter value.
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
- Cadence reference correspondence: voltage-domain logic should publish
  thresholds, output levels, initial state, and transition timing; ADC examples
  require bit/order/event semantics to be public.

## Validation

- EVAS hidden gold: PASS.
- EVAS negative variants: 4/4 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: 4/4 rejected.
- AHDL lint triage: no `AHDLLINT-*` findings. Spectre reported only
  `VACOMP-2435` and `SPECTRE-592` environment/mode warnings.
