# Two-Gate SOP Audit: Task 275 Divide By Two Toggle

## Scope

Task 275 is the canonical divide-by-two edge-toggle row after manual review of
the duplicate-title pair 184/275.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 275 as the canonical independent L1
  divide-by-two toggle row; keep task 184 only as a non-counted
  duplicate/migration artifact unless rewritten.
- Function boundary: `out` starts low, toggles on each rising crossing of
  `clk` through `vth`, and drives either `0` or `vdd` through the public
  transition parameters.
- Distinctness policy: task 275 does not gain independent coverage from task
  184; it replaces task 184 as the counted row for this function.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the canonical audited
  artifact.
- Prompt hygiene: the public prompt now removes historical source-provenance
  wording and exposes interface, initial state, rising-edge semantics, output
  levels, threshold, delay, transition time, and modeling constraints.
- Gold quality: the gold model uses `@(initial_step)` for low-state
  initialization, `@(cross(V(clk)-vth,+1))` for edge detection, and a voltage
  contribution through `transition(...)`.
- Checker role: the checker now derives expected output state from detected
  rising input edges, so visible and hidden stimuli can differ without changing
  checker code.
- Functional-math invariant: with initial state low, the expected output state
  is high after an odd number of rising edges and low after an even number.
- Cadence reference correspondence: local Cadence Verilog-AMS course material
  gives concrete examples for `@(initial_step)` initialization,
  `@(cross(...,+1))` threshold events, and `transition(state*Vdd, td, tr)` style
  output driving. Task 275 follows that event/state/transition pattern; the
  benchmark-specific part is only the divide-by-two state update.

## Evidence

- Human confirmation: user confirmed only one divide-by-two toggle row should
  remain counted; task 275 is retained as canonical.
- Visible/hidden relationship: hidden stimulus now uses a different edge
  schedule and stop time from the visible smoke deck.
- EVAS gold after dynamic-checker repair: PASS
  (`/private/tmp/v3_smoke_275_div2_after.json`).
- EVAS negatives after dynamic-checker repair: 4/4 `FAIL_SIM_CORRECTNESS`
  (`/private/tmp/v3_evas_div2_negatives_after.json`).
- Spectre gold after dynamic-checker repair: visible PASS and hidden PASS
  (`/private/tmp/v3_spectre_div2_visible_after.json`,
  `/private/tmp/v3_spectre_div2_hidden_after.json`).
- Spectre negatives after dynamic-checker repair: 4/4 `NEGATIVE_REJECTED`
  (`/private/tmp/v3_spectre_div2_negatives_after.json`).
- AHDL lint/read-in triage: no `AHDLLINT-*` messages were found in the
  visible, hidden, or negative Spectre work roots for this repair.
