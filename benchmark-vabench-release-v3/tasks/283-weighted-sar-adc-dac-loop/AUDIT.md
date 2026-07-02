# Weighted SAR ADC DAC Loop Audit

- Gate 1: L2 core flow retained. The row composes sample/hold, SAR conversion,
  public trial monitors, final code bits, and weighted DAC reconstruction.
- Gate 2: EVAS-ready for current public assets, Cadence lint/Spectre pending.
  Public prompt was lightly normalized to the current section names without
  changing the existing flow contract.
- Hidden coverage: existing hidden flow is distinct from the visible smoke deck
  and keeps the longer converter-loop validation.
- Checker: flow-level checker verifies public SAR/DAC consistency, range,
  code coverage, trial visibility, and monotonic reconstruction behavior.
- Negatives: stuck-zero flow variant is rejected by the behavior checker.
- EVAS note: this L2 flow needs a longer timeout than small single-DUT rows; a
  120 s timeout can expire, while a 360 s timeout passes on this host.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
