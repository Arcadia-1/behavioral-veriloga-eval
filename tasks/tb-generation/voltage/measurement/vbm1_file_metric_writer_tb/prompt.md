# Task: vbm1_file_metric_writer_tb

Write a Spectre testbench for a file metric writer DUT.

The DUT module is `file_metric_writer` with ports `vin, done`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `file_metric_writer.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Open a text metric file at startup using a string parameter named `filename` with default `metric.out`.
- On the first rising crossing of `vin` through 0.45 V, write the crossing time to the metric file and set `done` high.
- Keep `done` low before the first crossing and high afterwards; drive it with smoothed voltage transitions.

Stimulus and observability requirements:
- Drive `vin` through exactly one public rising crossing near 30 ns.
- Run to a later safe window and save `vin` and `done`; the file side effect is supporting evidence, not the only metric.

Review caveat: This is a normal measurement/file-output task. It is not a bugfix task; atomic file I/O semantics belong in EVAS/Spectre conformance.

Return exactly one Spectre testbench file named `tb_file_metric_writer_ref.scs`.
