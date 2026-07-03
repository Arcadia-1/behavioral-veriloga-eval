# Honest SOP Audit: Task 091 AGC Receiver Leveling Loop

## Scope

Task boundary is one Verilog-A DUT, `agc_receiver_leveling_loop.va`. Public
solver materials are `instruction.md`, `starter/`, and `test_visible/`.
Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and
`negative_variants/`.

## Gate 1

- Admission label: `l2_core_ready`.
- Function: composed RF/AFE receiver AGC flow with gain path, envelope/RSSI
  observation, gain-control update, leveled output, gain monitor, RSSI monitor,
  and lock-quality metric.
- Duplicate/counting policy: keep as L2 core. It is not a duplicate of LNA/PA
  gain-compression L1 rows because the benchmark evaluates closed-loop leveling
  and intermediate observability, not a single static gain-compression macro.

## Gate 2

- Modeling status: `cadence_modeling_ready`.
- Prompt contract: public interface, parameters, reset behavior, target
  amplitude/deadband, gain update direction, bounded output, `gain_mon`,
  `rssi_mon`, and metric semantics are stated without hidden-evaluator or
  `tb-generation` migration wording.
- Public/private split: visible decks are short public smoke scenarios for
  wiring and saved observables; hidden decks retain the longer behavioral AGC
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
