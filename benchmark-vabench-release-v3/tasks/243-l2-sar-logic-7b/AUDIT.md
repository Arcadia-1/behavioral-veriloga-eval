# Source L2 SAR Logic 7b Audit

- Source: `yueyh/L2_7bit_sar_logic.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: 7-bit asynchronous SAR logic with CLKS reset, CLKC conversion start, DCMPP/DCMPN pulse decisions, DO outputs, and positive/negative CDAC controls.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks, parity pass, and negative variant rejection.
- Evaluation: stable sampled logic behavior from `tran.csv`; raw simulator timestep equality is not used.
