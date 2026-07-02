# Two-Gate SOP Audit: Task 292 Hysteretic Comparator Receiver

## Scope

Task 292 has been rewritten from a smooth tanh comparator variant into a
Cadence-derived hysteretic comparator receiver. The public function is a
voltage-domain comparator receiver with differential input, upper/lower
hysteresis thresholds, fixed propagation delay, and a rail-coded output.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready` pending final human counting
  confirmation.
- Independence evidence: task 146 covers a smooth continuous tanh transfer;
  task 047 covers a simple threshold comparator; task 031 covers hysteretic
  complementary outputs without a fixed receiver delay; task 041 covers
  clocked/dynamic comparator delay behavior. Task 292 now evaluates an
  asynchronous hysteretic receiver with fixed output delay and rail-coded
  single-ended output.
- Human decision carried forward: the old 146/292 smooth-tanh overlap was not
  independently countable. Rewriting 292 into a hysteretic receiver is the
  proposed independent-coverage path.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after bridge-backed Spectre gold
  and negative validation. The result JSON reports no task-level errors; the
  remaining Spectre warnings are global AHDL-CMI/environment or simulator-mode
  notices rather than task-specific Verilog-A modeling findings.
- Cadence reference correspondence: Cadence Behavioral Modeling with
  Verilog-AMS comparator examples use analog differential inputs, `OFFSET` and
  `HYST`, upper/lower thresholds, and event-driven state changes. This
  benchmark keeps that threshold/state pattern but adapts the output from a
  Verilog-AMS `logic` port to a voltage-domain rail-coded `out` node for the
  current vaBench/EVAS scope.
- Prompt hygiene: the prompt uses the current public format and avoids old
  source names, hidden-checker wording, and implementation-history notes.
- Gold quality: the gold model declares all ports and overrideable parameters,
  initializes state from the differential input, updates state only on public
  threshold crossings, and drives a delayed `transition()` from a
  piecewise-constant state.
- Negative strength: five concrete negatives reject stuck output, missing
  hysteresis, missing delay, wrong polarity, and wrong output level.

## Evidence

- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` and
  `test_hidden/tests/tb_source_ref.scs` use different differential waveforms
  and timing while preserving the public default threshold/delay contract.
- EVAS gold: visible PASS and hidden PASS using `runners/simulate_evas.py`
  with `VAEVAS_EVAS_REPO` pointed at the local EVAS checkout and
  `--checker-task-id v3_hysteretic_comparator_receiver`. The checker reported
  four expected hysteresis/delay edges, zero delay error, and zero
  settled-level error on both decks.
- EVAS negatives: 5/5 behavioral rejections using the hidden deck. All five
  variants compiled the DUT and testbench, then failed `sim_correct` for the
  intended behavior class: stuck-low output, missing hysteresis, missing delay,
  wrong polarity, and wrong output level.
- Spectre gold: hidden PASS using the restored Virtuoso bridge
  (`BRIDGE_PROFILE=jin`, `--spectre-backend bridge`). The checker reported four
  expected hysteresis/delay edges with sub-picosecond delay error and zero
  settled-level error.
- Spectre negatives: 5/5 `NEGATIVE_REJECTED` on the hidden deck. The completed
  bridge rerun rejects stuck-low output, missing hysteresis, missing delay,
  wrong polarity, and wrong output level.
- AHDL lint/read-in triage: Spectre reports no task-level errors. The remaining
  warnings are global AHDL-CMI/environment or simulator-mode notices, not
  task-specific Verilog-A modeling findings.
