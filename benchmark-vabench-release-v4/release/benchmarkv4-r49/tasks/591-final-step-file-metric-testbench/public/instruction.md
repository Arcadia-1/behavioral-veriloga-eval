# Final Step File Metric Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Final Step File Metric` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.

## Public Verilog-A Interface

- Artifact `final_step_file_metric_ref.va`:
  - Module `final_step_file_metric_ref` (entry)
    - position 0: `VDD` (inout, electrical)
    - position 1: `VSS` (inout, electrical)
    - position 2: `ref` (input, electrical)
    - position 3: `metric_out` (output, electrical)

Stable public Spectre binding:

The submitted `testbench.scs` must use the supplied DUT through this public binding:

- Include path: `./dut/final_step_file_metric_ref.va`
- DUT instance: `IDUT (vdd vss ref metric_out) final_step_file_metric_ref`
- Required saved public traces: `vdd`, `vss`, `ref`, `metric_out`
- Use one bounded transient analysis with a finite positive stop time.

You must design the stimulus yourself. Save traces as bare public signal names
(for example `clk`, not suffixed or hierarchical forms such as `clk:V` or
`XDUT.clk`). Do not redefine the DUT, drive DUT output nets, save
hierarchical/private nodes, or use checker/gold/internal files.

## Public Parameter Contract

- `final_step_file_metric_ref.vth` defaults to `0.45` V; valid range: finite real within the VSS-to-VDD logic range; sets ref rising-crossing threshold relative to VSS.
- `final_step_file_metric_ref.tedge` defaults to `2e-10` s; valid range: tedge > 0; sets metric_out transition smoothing.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_ZERO_INITIAL_STATE`: exercise and make observable: Before any qualifying ref edge, the event count and metric_out are zero. Required traces: `time`, `ref`, `metric_out`.
- `P_RISING_EDGE_COUNT`: exercise and make observable: Every rising ref crossing through vth increments the retained event count exactly once; falling crossings do not. Required traces: `time`, `ref`, `metric_out`.
- `P_NORMALIZED_METRIC`: exercise and make observable: Metric_out equals the VDD-to-VSS rail span multiplied by the retained event count divided by four. Required traces: `time`, `vdd`, `vss`, `ref`, `metric_out`.
- `P_EVENT_UPDATED_OUTPUT`: exercise and make observable: Metric_out changes only after counted rising events and uses finite transition smoothing of the retained target. Required traces: `time`, `ref`, `metric_out`.
- `P_FINAL_TEXT_RECORD`: exercise and make observable: At final_step, the module emits one text metric record to candidate.out in the simulator working directory with format count=<integer> metric=<fixed-point to three decimals>. Required traces: `time`, `ref`, `metric_out`.


The following canonical public behavior is normative for this derived form:

Write a pure voltage-domain measurement helper that counts rising reference
events during transient simulation, exposes a voltage-coded metric, and writes
the final metric at `final_step`.

Required observable behavior:

- Initialize the event count and metric to zero.
- On every rising crossing of `ref` through `vth`, increment the event count.
- Expose the normalized metric as `metric_out = V(VDD,VSS) * count / 4`.
- At `final_step`, write exactly one text metric record to the public basename
  `candidate.out` in the simulator working directory. The record format is
  `count=<integer> metric=<fixed-point>` and the metric value is the final
  normalized count divided by four, formatted to three digits after the decimal
  point.

Use voltage-coded logic referenced to `VDD` and `VSS`. Smooth only event-updated
metric state; do not feed a continuously varying branch expression directly
into `transition()`. Do not generate a Spectre testbench, waveform files,
validation artifacts, transistor-level devices, current contributions, `ddt()`, or
`idt()`.


The required trace names are: `time`, `vdd`, `vss`, `ref`, `metric_out`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the declared `./dut/...` source paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
