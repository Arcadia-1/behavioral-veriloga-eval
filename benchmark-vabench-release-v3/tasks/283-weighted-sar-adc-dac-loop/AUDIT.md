# Weighted SAR ADC DAC Loop Audit

- Gate 1: L2 core flow retained. The row composes sample/hold, SAR conversion,
  public trial monitors, final code bits, and weighted DAC reconstruction.
- Gate 2: `cadence_modeling_ready` for current public assets.
  Public prompt was normalized to state the L2 flow role, separate exact
  testbench stimulus values from DUT-internal circuit contracts, and expose the
  observable SAR trial monitors without leaking checker sample windows.
- Hidden coverage: existing hidden flow is distinct from the visible smoke deck
  and keeps the longer converter-loop validation.
- Checker: flow-level checker verifies public SAR/DAC consistency, range,
  code coverage, trial visibility, and monotonic reconstruction behavior.
- Negatives: stuck-zero flow variant is rejected by the behavior checker.
- EVAS note: this L2 flow needs a longer timeout than small single-DUT rows; a
  120 s timeout can expire, while a 360 s timeout passes on this host.
- Visible deck note: the public visible SCS was aligned with the public prompt
  by running the same 20 us full-swing sine scenario as the L2 contract. The
  previous 2 us smoke length produced only 12 completed conversions and was too
  short for the flow-level coverage checker.
- Cadence reference correspondence: Cadence converter examples model the same
  pieces as public behavior rather than private checker facts: sample/hold
  capture on a clock event, thresholded bit-bus DAC reconstruction, MSB-to-LSB
  ADC decision sequencing, and explicit transition-smoothed observable outputs.
  This row combines those conventions into an integrated conversion loop.
- Cadence/Spectre: visible gold PASS, hidden gold PASS, and hidden
  `neg_001_stuck_zero` rejected in the closeout bridge run. AHDL triage found no
  task-level `AHDLLINT-*` messages or AHDL compile errors; only the global
  `VACOMP-2435` environment warning appears.
