# Update-Latched Mux4 Sampler Audit

- Gate 1 status: `hard_duplicate_rewrite_or_remove` rescued to `independent_l1_ready` pending final PR review.
- Rescue note: the original row duplicated `170-clocked-four-input-mux`. It is now a resettable, update-qualified mux sampler: select changes are latched only on update-qualified falling clock edges, reset forces the default `din0` path, and update-low edges hold the previous sampled output.
- Cadence reference rationale: this follows the event-capture / DFF / sample-and-hold pattern from the Cadence modeling material, with thresholded events and transition-shaped held outputs.
- Counting recommendation: can be counted separately from `170` because the public function now includes reset default selection and glitch-free update qualification rather than a plain clocked 4:1 sample.
- Gate 2 repair: public prompt, starter, gold, visible/hidden decks, checker, and five behavioral negatives now agree on reset/update-qualified mux sampling.

- Source: `zhangm/MUX4T1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: resettable, update-qualified four-input mux sampler used for glitch-free AMS control selection.
- Import status: repaired from a duplicate imported row into an AMS-facing control task.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - EVAS2 gold semantic validation: PASS.
  - EVAS2 negative variants: five behavioral negatives rejected.
  - EVAS AHDL-like lint preflight: PASS with zero diagnostics.
  - Spectre AX gold semantic validation: PASS; only environment/bridge warnings observed, no task-specific AHDL errors.
