# 4-bit Self-Timed SAR Logic Audit

- Scope: L1 data-converter DUT. This is a self-timed SAR controller, not a complete ADC loop.
- Source provenance: `zhangz/L3_logic_4b.va` from the exact-deduplicated historical Verilog-A corpus.
- Gate 1 content review: Retain. The task covers a comparator-clock handshake and bottom-plate control updates that are independent from pure DAC weighting tasks.
- Gate 2 prompt/checker review: Public prompt now states the exact interface, supply-derived logic threshold, reset state, comparator pulse sequencing, and default logic delay. Hidden stimulus is distinct from the visible smoke deck.
- Verification: EVAS gold passed; all four negative variants were rejected. Spectre hidden gold passed with the same behavior checker. AHDL log triage found no task-level `AHDLLINT-*` messages or AHDL compile errors.
