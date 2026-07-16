# Rail Normalized Metric Mapper Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Rail Normalized Metric Mapper` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.

## Public Verilog-A Interface

- Artifact `rail_normalized_metric_mapper.va`:
  - Module `rail_normalized_metric_mapper` (entry)
    - position 0: `meas` (input, electrical)
    - position 1: `vdd` (input, electrical)
    - position 2: `vss` (input, electrical)
    - position 3: `en` (input, electrical)
    - position 4: `norm` (output, electrical)
    - position 5: `valid` (output, electrical)

Stable public Spectre binding:

The submitted `testbench.scs` must use the supplied DUT through this public binding:

- Include path: `./dut/rail_normalized_metric_mapper.va`
- DUT instance: `XDUT (meas vdd vss en norm valid) rail_normalized_metric_mapper`
- Required saved public traces: `en`, `meas`, `norm`, `valid`, `vdd`, `vss`
- Use one bounded transient analysis with a finite positive stop time.

You must design the stimulus yourself. Save traces as bare public signal names
(for example `clk`, not suffixed or hierarchical forms such as `clk:V` or
`XDUT.clk`). Do not redefine the DUT, drive DUT output nets, save
hierarchical/private nodes, or use checker/gold/internal files.

## Public Parameter Contract

- `rail_normalized_metric_mapper.vth` defaults to `0.45`; valid range: finite; overrides vth.
- `rail_normalized_metric_mapper.vhi` defaults to `0.9`; valid range: finite; overrides vhi.
- `rail_normalized_metric_mapper.span_min` defaults to `0.60`; valid range: finite; overrides span_min.
- `rail_normalized_metric_mapper.span_max` defaults to `1.20`; valid range: finite; overrides span_max.
- `rail_normalized_metric_mapper.tr` defaults to `50p`; valid range: finite; overrides tr.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_NORMALIZE_MEAS_RELATIVE_TO_THE_LOCAL`: exercise and make observable: Let `span = V(vdd, vss)` and `local_meas = V(meas) - V(vss)`. When `V(en) > vth` and `span >= span_min`, `norm = vhi * clip01(local_meas / span)`. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_CLIP_THE_NORMALIZED_METRIC_TO_THE`: exercise and make observable: `clip01(x)` limits `x` to `[0, 1]`, so enabled `norm` is clipped to `[0 V, vhi]` even when `meas` lies outside the local rails. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_ASSERT_VALID_ONLY_WHEN_ENABLE_IS`: exercise and make observable: `valid = vhi` exactly when `V(en) > vth`, `span_min <= span <= span_max`, and `0 <= local_meas <= span`; otherwise `valid = 0 V`. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_CLEAR_NORM_AND_VALID_WHILE_DISABLED`: exercise and make observable: Disabled or `span < span_min` clears both outputs. A span above `span_max` clears `valid` but does not by itself clear clipped `norm`. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: exercise and make observable: Use local analog helper functions rather than user task/endtask syntax. Required traces: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.

The required trace names are: `time`, `en`, `meas`, `norm`, `valid`, `vdd`, `vss`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the declared `./dut/...` source paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
