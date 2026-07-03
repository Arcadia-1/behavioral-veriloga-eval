# Honest SOP Audit: Task 043 RF Mixer Downconverter Macro

## Scope

Task boundary is one Verilog-A DUT, `rf_mixer_downconverter_macro.va`.
Public solver materials are `instruction.md`, `starter/`, and `test_visible/`.
Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and
`negative_variants/`.

## Gate 1

- Admission label: `independent_l1_ready`.
- Function: RF/AFE voltage-domain downconverter macro. It multiplies the input
  envelope deviation from common mode by LO polarity, preserves common mode,
  bounds the baseband output, and exposes a conversion activity metric.
- Duplicate/counting policy: keep as a standalone L1. It is not a duplicate of
  task 103 because this row evaluates a single reusable mixer macro, while 103
  evaluates a composed quadrature I/Q chain.

## Gate 2

- Modeling status: `cadence_modeling_ready`.
- Prompt contract: public interface, parameters, reset behavior, LO polarity,
  conversion-gain semantics, bounded voltage-domain output, and metric role are
  stated without hidden-checker, old migration, or gold-history wording.
- Public/private split: public visible smoke is wiring/compile coverage only;
  hidden validation checks the longer behavioral conversion windows.

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
