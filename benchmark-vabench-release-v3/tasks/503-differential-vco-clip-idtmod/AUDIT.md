# SOP Audit: Differential VCO With Clip And Idtmod

## Scope

PLL clock-and-timing extension task. Pure voltage-domain behavioral DUT that
implements a fully differential sine VCO with differential control voltage,
clipped instantaneous frequency, `idtmod()` phase integration, and opposite
output arms around a common-mode voltage.

## Review Findings

- Gate 1: `independent_l1_rework` until upstream decides whether PLL extension
  candidates are counted outside the original full-300 denominator.
- Gate 2: `cadence_modeling_ready_evas2_pending`; targeted Spectre simulation
  and real Cadence `spectre -ahdllint +diagnose` visible/hidden runs pass.
  Current EVAS2 full-model execution rejects the continuous clipped-frequency
  `idtmod()`/`sin()` VCO row with `no_event_transition_ir`. EVAS AHDL-like lint
  also reports conservative static warnings around the continuous expression,
  but Spectre reports no task-level lint issue for this modeling pattern.
- Prompt hygiene: removed private evaluator wording and described the clamp as
  public circuit behavior rather than checker-only behavior.
- Artifact boundary: target is only `differential_vco_clip_idtmod.va`; no
  support artifact is required.
- Functional invariant: `Fnom + dFdV*V(vinp,vinm)` is clamped into
  `[Fmin,Fmax]`, then integrated with `idtmod()`; `outp` and `outm` must be
  symmetric around `Vcm`.
- Coverage repair: hidden stimulus now drives raw frequency above `Fmax`, so
  the checker exercises the upper clamp behavior instead of only relying on a
  structural `clip(` syntax guard.

## Checker Context

- Checker id: `v3_503_differential_vco_clip_idtmod`.
- The checker reintegrates clipped phase from the differential input and
  compares both output arms plus the wrapped-phase metric.
- The release `CHECKS.yaml` intentionally does not enable `sim_correct` for
  this row yet. Re-enable it only after EVAS2 can execute this VCO pattern and
  reject the negative variants behaviorally.

## Validation Status

Fresh validation from this clean branch:

- EVAS2 gold/negative: pending. Current strict EVAS2 execution rejects the gold
  with `no_event_transition_ir`, so this row is not behavior-certified by EVAS2.
- EVAS AHDL-like lint preflight: WARN on `clip()`/`idtmod()`/`sin()` continuous
  expression classification; no compatibility errors.
- Spectre simulation: visible gold PASS, hidden gold PASS with upper clamp
  exercised, and five hidden negative variants rejected.
- Cadence `spectre -ahdllint +diagnose`: visible and hidden decks PASS with
  zero task-level AHDL lint issues. Both logs report "No lint issue detected in
  the simulation." Remaining warnings are environment/setup notices
  (`VACOMP-2435` for unsupported `CDS_AHDLCMI_ENABLE`, `SPECTRE-592` for
  ignored/redefined Spectre X parameters), not task-specific modeling issues.
