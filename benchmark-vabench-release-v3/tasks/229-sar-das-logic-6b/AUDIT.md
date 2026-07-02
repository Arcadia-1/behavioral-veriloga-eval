# 6-bit SAR DAS Logic Audit

- Scope: L1 data-converter DUT. This is SAR differential bit-control logic for a converter control path.
- Source provenance: `zhangz/SAR_logic_DAS_va.va` from the exact-deduplicated historical Verilog-A corpus.
- Gate 1 content review: Retain. The task is distinct from analog DAC-weight tasks because it exercises sampling refresh, MSB-to-LSB SAR state progression, and complementary control/pulse outputs.
- Gate 2 prompt/checker review: Public prompt now states the module interface, public parameters, sampling-clock reset/preset semantics, comparator decision polarity, and `co/cob` pulse behavior. Hidden stimulus is distinct from the visible smoke deck.
- Verification: EVAS gold passed; all four negative variants were rejected. Spectre hidden gold passed with the same behavior checker. AHDL log triage found no task-level `AHDLLINT-*` messages or AHDL compile errors.
