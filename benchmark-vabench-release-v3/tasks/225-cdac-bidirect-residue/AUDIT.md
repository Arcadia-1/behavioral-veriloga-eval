# CDAC Bidirectional Residue Audit

- Scope: L1 data-converter DUT. This is a SAR/CDAC residue helper, not a generic simulator-syntax task.
- Source provenance: `caiyizeng25/cdac_ideal_bidirect.va` from the exact-deduplicated historical Verilog-A corpus.
- Gate 1 content review: Retain. The task covers a sampled CDAC residue update with a positive MSB step and binary-weighted subtractive control steps.
- Gate 2 prompt/checker review: Public prompt now states the module interface, sampled residue behavior, control-edge polarity, and modeling boundary. Hidden stimulus is distinct from the visible smoke deck.
- Verification: EVAS gold passed; all four negative variants were rejected. Spectre hidden gold passed with the same behavior checker. AHDL log triage found no task-level `AHDLLINT-*` messages or AHDL compile errors.
