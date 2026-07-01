# File Fscanf Multi Column Profile

Implement one behavioral Verilog-A source file named `file_fscanf_multi_column_profile.va`.

## Interface

Use this exact module interface:

```verilog
module file_fscanf_multi_column_profile (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

Keep the model behavioral and do not introduce current contributions. The source must read the sidecar file `stimulus_profile.txt`.

## Required Behavior

Use $fscanf() to ingest a multi-column behavioral profile.

Required behavior:

- open `stimulus_profile.txt` during `initial_step`;
- read the first row with `$fscanf(fd, "%f %f %f", prof_t, prof_v, prof_gain)`;
- close the file after reading;
- when three values are read, initialize `out_v` to `prof_v` and `metric_v` to the read count;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and the internal count when `rst` is high;
- otherwise drive `out_v = prof_v` and `metric_v = prof_t + prof_gain`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_fscanf_multi_column_profile.va`.
