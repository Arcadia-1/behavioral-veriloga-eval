# Task 092 Audit

Task: `092-amplifier-filter-chain`

Status: `l2_core_ready` candidate after prompt/checker repair. Gate 2 Cadence
status is `cadence_modeling_ready` for the reviewed gold after current-branch
EVAS, targeted Spectre, and AHDL warning triage. This row should be counted as
an integration-flow L2, not as a duplicate L1 filter row.

## Duplicate/Counting Policy

Keep as L2 core. The row overlaps intentionally with L1 amplifier and low-pass
building blocks, but the benchmark contract evaluates the composed chain:
bounded preamplifier, two cascaded sampled low-pass states, monitor consistency,
output lag, reset recovery, and a settling metric. It should not be counted as
another standalone filter primitive.

## Review Decision

- Useful scenario: pass. The row is a composed baseband chain: bounded
  preamplifier, two cascaded sampled low-pass states, monitor outputs, and a
  settling metric.
- Counting decision: keep as an L2 integration-flow row, not as another
  standalone gain or low-pass primitive. The independent value is the combined
  preamp/filter/settling monitor interaction across multiple public
  observables.
- Reasonable task: pass after repair. The public prompt now describes the
  target DUT, nine-port interface, reset/clock behavior, monitor semantics, and
  observable flow-level contract.
- Complete tests: pass for EVAS/Spectre gold validation and EVAS negative
  recertification. The public smoke deck is now a short wiring/compile
  scenario, while the private validation deck exercises the longer flow. The
  behavior checker now requires all nine observables.
- Fair evaluation: pass. The checker verifies the public flow behavior and
  monitor consistency rather than accepting only the main output.

## Checker Contract

- Checker id: `v3_092_amplifier_filter_chain`.
- Required trace signals: `time`, `clk`, `rst`, `vin`, `out`, `metric`,
  `preamp_mon`, `filt1_mon`, `filt2_mon`, and `settle_metric`.
- Behavioral checks: preamp and metric windows, first-stage vs second-stage
  lag, output-to-filter consistency, voltage-coded settling flag, reset
  recovery, and range sanity.

## Current Evidence

- Reference solution: PASS under EVAS and targeted Spectre with the
  strengthened checker.
- Concrete negatives: 5/5 rejected with behavioral failures after checker
  strengthening.
- Public visible smoke: EVAS compile/transient smoke PASS.
- AHDL lint/read-in triage: EVAS AHDL-like lint preflight reports PASS with
  zero diagnostics for both hidden solution decks. Spectre AHDL read-in reports
  no task-level `AHDLLINT-*`, AHDL compile, or VACOMP errors; the remaining
  `VACOMP-2435` and `SPECTRE-592` warnings are shared environment/mode notices.
