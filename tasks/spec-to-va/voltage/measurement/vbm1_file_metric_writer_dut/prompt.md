# Task: vbm1_file_metric_writer_dut

Write a pure voltage-domain Verilog-A module for a file metric writer.

The DUT module is `file_metric_writer` with ports `vin, done`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Open a text metric file at startup using a string parameter named `filename` with default `metric.out`.
- On the first rising crossing of `vin` through 0.45 V, write the crossing time to the metric file and set `done` high.
- Keep `done` low before the first crossing and high afterwards; drive it with smoothed voltage transitions.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Review caveat: This is a normal measurement/file-output task. It is not a bugfix task; atomic file I/O semantics belong in EVAS/Spectre conformance.

Return exactly one complete Verilog-A file named `file_metric_writer.va`.
