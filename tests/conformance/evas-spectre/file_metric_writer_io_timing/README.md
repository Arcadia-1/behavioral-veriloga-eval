# file_metric_writer_io_timing

## Purpose

This conformance asset isolates external file-output side effects from a
Verilog-A behavioral model. It comes from the historical
`vbm1_file_metric_writer_bugfix` main120 row, but it is not a public bugfix
benchmark task.

## Semantic Axis

- Axis: `checker-semantics`
- Expected EVAS/Spectre relation: `binary_outcome_equal`
- Scope: one `$fopen` at `initial_step`, one `$fwrite` on the first positive
  `cross(V(vin)-vth)`, and a `done` voltage flag that mirrors whether the file
  write has happened.

## Gold Evidence

- `gold/file_metric_writer.va`
- `gold/tb_file_metric_writer_ref.scs`
- `gold/expected_metric.out`

The input PWL rises from `0 V` at `30 ns` to `0.9 V` at `31 ns`, so the public
crossing target is approximately `30.5 ns` for `vth=0.45`.

## Why This Is Not A Normal Bugfix Task

The important behavior is the simulator/harness treatment of an output file
artifact, not a model repair pair. A normal bugfix task would require a
reviewed bad source whose single functional defect causes a model-level failure
and a fixed source that repairs it. This case instead asks whether EVAS and
Spectre expose the same pass/fail result for file metric production.

## Runner Hook Needed

A conformance runner should:

1. run the included testbench on both EVAS and Spectre;
2. require both runs to compile and finish;
3. collect the metric file from each run directory;
4. parse the first numeric token after `cross`;
5. require exactly one metric record near `30.5 ns`, with a tolerance such as
   `1 ps`;
6. require `done` to be low before the crossing and high after the crossing.

The parser should compare structured metric values rather than exact file bytes,
because newline and string-escape rendering may differ across simulators.
