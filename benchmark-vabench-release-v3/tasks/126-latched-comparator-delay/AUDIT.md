# Audit: 126-latched-comparator-delay

## Gate 1

- Label: `independent_l1_ready`.
- Function: supply-referenced latched comparator with configurable output delay,
  input-referred offset, and deterministic/noisy decision hook.
- Independence: retained as distinct from `112` because this task has a single
  latched output, derives output rails from `GND`/`VDD`, and includes delay plus
  offset/noise decision semantics.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: replaced terse import prompt with a public circuit contract.
- Public contract now exposes module/ports, `td`, `tr`, `vos`, `vn`,
  `seed_init`, supply-derived threshold/output rails, latch edge, and
  deterministic `vn=0` behavior.
- Visible/hidden relationship: hidden testbench is no longer byte-identical to
  visible smoke; hidden coverage sets `vos=50m`, `vn=0`, a non-default delay,
  and an input case where `VINP > VINN` but the differential is below offset.
- Checker: `v3_latched_comparator_delay`, stable-window samples for high/low
  decisions after delay.
- Functional sanity vectors:
  - `VINP - VINN = 110m`, `vos=50m`: output high after the latch delay.
  - `VINP - VINN = 30m`, `vos=50m`: output low despite `VINP > VINN`.
  - `VINP - VINN = 100m`, `vos=50m`: output high.
  - Negative differential: output low.
- Cadence reference correspondence: random/distribution semantics must publish
  seed and distribution behavior; voltage-domain logic must publish thresholds,
  output levels, initial state, and transition timing.

## Validation

- EVAS hidden gold: PASS.
- EVAS negative variants: 4/4 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: 4/4 rejected.
- AHDL lint triage: no `AHDLLINT-*` findings. Spectre reported only
  `VACOMP-2435` and `SPECTRE-592` environment/mode warnings.
