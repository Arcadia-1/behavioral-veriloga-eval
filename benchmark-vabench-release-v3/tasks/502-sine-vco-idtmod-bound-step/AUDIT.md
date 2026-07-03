# SOP Audit: Sine VCO With Idtmod And Bound Step

## Scope

PLL clock-and-timing extension task. Pure voltage-domain behavioral DUT that
implements a continuous-time sine VCO with an `idtmod()` modulo-1 phase
integrator and a `$bound_step()` points-per-cycle timestep request.

## Review Findings

- Gate 1: `independent_l1_rework` until upstream decides whether PLL extension
  candidates are counted outside the original full-300 denominator.
- Gate 2: `cadence_modeling_ready_evas2_behavior_checked`; EVAS AHDL-like lint
  is clean, targeted Spectre simulation passes, and strict EVAS2 gold/negative
  behavior verification passes when run against the continuous `idtmod()`/`sin()`
  VCO support from Arcadia-1/EVAS#69 or an equivalent merged commit. A separate
  `spectre -ahdllint` oracle run has not been recorded in this public audit.
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
- The release `CHECKS.yaml` enables `sim_correct` for this row. Promotion
  remains an extension claim outside the original full-300 denominator and
  depends on EVAS continuous `idtmod()`/`sin()` support.

## Validation Status

Fresh validation from this clean branch:

- EVAS2 gold/negative: PASS with the local EVAS continuous `idtmod()`/`sin()`
  support branch. In the paired 502/503 run, 2/2 gold cases pass and 10/10
  negative variants are rejected with 0 expectation failures.
- EVAS AHDL-like lint preflight: visible and hidden decks PASS with zero
  diagnostics.
- Spectre simulation: visible gold PASS, hidden gold PASS, and five hidden
  negative variants rejected.
- Cadence `spectre -ahdllint`: not run as a separate oracle in this PR.
