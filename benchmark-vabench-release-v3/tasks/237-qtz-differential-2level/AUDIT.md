# Differential Two-Level Quantizer Audit

- Scope: L1 data-converter DUT. This is a clocked quantizer primitive for converter modeling.
- Source provenance: `zhangsh/QTZ.va` from the exact-deduplicated historical Verilog-A corpus.
- Gate 1 content review: Retain. The task is distinct from flash-code summarizers and DAC tasks because it samples a differential input and holds a signed two-level code.
- Gate 2 prompt/checker review: Public prompt now states the exact interface, clock-edge sampling, midpoint reference threshold, signed `-0.5/+0.5` output levels, and hold behavior. Hidden stimulus is distinct from the visible smoke deck.
- Verification: EVAS gold passed; all four negative variants were rejected. Spectre hidden gold passed with the same behavior checker. AHDL log triage found no task-level `AHDLLINT-*` messages or AHDL compile errors.
