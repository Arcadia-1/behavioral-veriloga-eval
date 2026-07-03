# SOP Audit: Charge Pump PFD State Machine

## Scope

PLL clock-and-timing extension task. Pure voltage-domain behavioral DUT that
implements a three-state phase-frequency detector with `@cross` edge events and
a sampled `@timer` control-voltage integrator.

## Review Findings

- Gate 1: `independent_l1_rework` until upstream decides whether PLL extension
  candidates are counted outside the original full-300 denominator.
- Gate 2: `cadence_lint_pending`; EVAS lint is clean and targeted Spectre
  simulation passes, but a separate `spectre -ahdllint` oracle run has not
  been recorded in this public audit.
- Prompt hygiene: removed private evaluator wording. The prompt now describes
  positive and negative phase offset behavior as public harness semantics.
- Artifact boundary: target is only `charge_pump_pfd_state_machine.va`; the
  harness supplies `ref_fb_clk.va` as support.
- Support repair: `ref_fb_clk.va` now allows signed `phase_lead`, matching the
  visible scenario where feedback leads reference.
- Checker repair: checker infers the lead/lag direction from waveform edges
  instead of assuming reference always leads.

## Checker Context

- Checker id: `v3_504_charge_pump_pfd_state_machine`.
- The checker determines whether reference or feedback leads, checks that
  `vctrl` moves toward the corresponding clamp rail, verifies clamp bounds, and
  checks metric polarity pulses in the late window.

## Validation Status

Fresh validation from this clean branch:

- EVAS gold/negative: gold PASS; five negative variants rejected.
- EVAS AHDL-like lint preflight: visible and hidden decks PASS with zero
  diagnostics.
- Spectre simulation: visible gold PASS, hidden gold PASS, and five hidden
  negative variants rejected.
- Cadence `spectre -ahdllint`: not run as a separate oracle in this PR.
