# Honest SOP Audit: Task 045 Soft Hysteretic Limiter

## Scope

Task boundary is one Verilog-A DUT, `soft_hysteretic_limiter.va`. Public solver
materials are `instruction.md`, `starter/`, and `test_visible/`.
Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and
`negative_variants/`.

## Gate 1

- Admission label: `independent_l1_ready`.
- Function: baseband soft limiter with clocked hysteresis memory, bounded
  output compression, and a voltage-coded state metric.
- Duplicate/counting policy: keep as a standalone L1. It is distinct from
  simple clamps or limiting amplifiers because the task requires stateful
  hysteresis memory across mid-level hold windows.

## Gate 2

- Modeling status: `cadence_modeling_ready`.
- Prompt contract: public interface, parameters, reset behavior, high/low memory
  states, output compression, transition smoothing, and metric semantics are
  stated without hidden-checker, old migration, or gold-history wording.
- Public/private split: public visible smoke is wiring/compile coverage only;
  hidden validation checks limiting levels, hysteresis memory, and metric span.

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
