# Source Pipe ADC Gain Control Loop Audit

- Source: `lixingyu/TEST_D2A_PIPE_ADC_GAIN_CAL.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: pipeline ADC backend gain-control loop that alternates plus/minus test DAC codes and updates a 7-bit gain control word.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch21-evas/232-source-pipe-adc-gain-control-loop`
  - `WORK/source-import-batch21-spectre/232-source-pipe-adc-gain-control-loop`
