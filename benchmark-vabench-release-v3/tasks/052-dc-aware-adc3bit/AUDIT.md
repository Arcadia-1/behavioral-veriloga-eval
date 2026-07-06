# DC Aware ADC3bit Audit

- Gate 1: `independent_l1_ready` as an issue #109 re-slot. This row is a
  static/combinational ADC model whose output is valid without a sampling clock,
  distinct from clocked ADC rows, DAC rows, and thermometer-bus source rows.
- Gate 2: `cadence_modeling_ready`. Public prompt exposes clipping, bin-floor
  quantization, bit order, output level, and transition timing without leaking
  checker sample windows. Post-re-slot validation passes EVAS hidden gold and
  rejects all five EVAS hidden negative variants. Spectre bridge validation
  passes visible and hidden gold, and hidden Spectre negatives reject all five
  variants. AHDL log triage found no task-level AHDL compile errors; only shared
  setup warnings such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence converter examples commonly model
  ideal ADC behavior by clipping or bounding the analog input, mapping it to a
  discrete code, and driving voltage-coded digital outputs. This candidate keeps
  the static conversion behavior explicit instead of adding a clocked sampling
  contract.
