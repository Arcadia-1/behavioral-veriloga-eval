# SOP Audit: Sine VCO With Idtmod And Bound Step

## Scope

PLL clock-and-timing extension task. Pure voltage-domain behavioral DUT that
implements a continuous-time sine VCO with an `idtmod()` modulo-1 phase
integrator and a `$bound_step()` points-per-cycle timestep request.

## Review Findings

- Gate 1: `independent_l1_rework` until upstream decides whether PLL extension
  candidates are counted outside the original full-300 denominator.
- Gate 2: `cadence_modeling_ready_evas2_pending`; EVAS AHDL-like lint is clean
  and targeted Spectre simulation passes, but current EVAS2 full-model
  execution rejects the continuous `idtmod()`/`sin()` VCO row with
  `no_event_transition_ir`. A separate `spectre -ahdllint` oracle run has not
  been recorded in this public audit.
- Prompt hygiene: removed private evaluator wording and fixed the old
  output-range mismatch. The public contract now states the output is a bipolar
  sine centered at 0 V.
- Artifact boundary: target is only `sine_vco_idtmod_bound_step.va`; no support
  artifact is required.
- Functional invariant: positive operating frequency is integrated with
  `idtmod(freq_q, 0, 1)`, `out` follows `vco_amp*sin(2*pi*phase_q)`, and
  `metric` follows `vco_amp*phase_q`.

## Checker Context

- Checker id: `v3_502_sine_vco_idtmod_bound_step`.
- The checker reintegrates phase from `V(vin)` with the shared modulo phase
  helper and compares `out` plus `metric` over a strided waveform window.
- `$bound_step()` is checked as a public syntax/modeling requirement. The
  Python EVAS backend does not use it as a timestep oracle, so checker evidence
  is functional phase/sine evidence plus syntax coverage, not an independent
  timestep-density proof.
- The release `CHECKS.yaml` intentionally does not enable `sim_correct` for
  this row yet. Re-enable it only after EVAS2 can execute this VCO pattern and
  reject the negative variants behaviorally.

## Validation Status

Fresh validation from this clean branch:

- EVAS2 gold/negative: pending. Current strict EVAS2 execution rejects the gold
  with `no_event_transition_ir`, so this row is not behavior-certified by EVAS2.
- EVAS AHDL-like lint preflight: visible and hidden decks PASS with zero
  diagnostics.
- Spectre simulation: visible gold PASS, hidden gold PASS, and five hidden
  negative variants rejected.
- Cadence `spectre -ahdllint`: not run as a separate oracle in this PR.
