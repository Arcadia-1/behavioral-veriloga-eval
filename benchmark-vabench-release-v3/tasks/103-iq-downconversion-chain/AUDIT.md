# Honest SOP Audit: Task 103 IQ Downconversion Chain

## Scope

Task boundary is one Verilog-A DUT, `iq_downconversion_chain.va`. Public solver
materials are `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only
materials are `solution/`, `test_hidden/`, `test_harness/`, and
`negative_variants/`.

## Gate 1

- Admission label: `l2_core_ready`.
- Function: composed voltage-domain I/Q downconversion chain with quadrature LO
  sequencing, LO polarity monitors, I/Q mixer monitors, filtered I-path output,
  Q-path metric, and phase monitor.
- Duplicate/counting policy: keep as L2 core. It is not a duplicate of task 043
  because this row evaluates quadrature sequencing and multi-observable I/Q
  chain integration, not only a single LO-polarity mixer macro.

## Gate 2

- Modeling status: `cadence_modeling_ready`.
- Prompt contract: public interface, parameters, reset behavior, four-phase
  quadrature sequence, `lo_i`/`lo_q`, `mix_i`/`mix_q`, `phase_mon`, I/Q
  baseband outputs, and common-mode recovery are stated without
  hidden-evaluator or `tb-generation` migration wording.
- Public/private split: visible decks are short public smoke scenarios for
  wiring and saved observables; hidden decks retain the longer behavioral I/Q
  validation flow.

## Verification

- Visible smoke: PASS.
- EVAS hidden gold: PASS.
- Concrete negative recertification: 5/5 expected failures, all failed
  behavioral correctness after compiling and simulating.
- AHDL-like lint preflight: solution hidden and starter visible slices report
  0 diagnostics.
- Targeted Spectre AX hidden gold: PASS. Spectre read-in reports no
  task-specific AHDL compile error, `AHDLLINT-*`, or `VACOMP-1116`; remaining
  warnings are shared environment/preset notices.
