# File Profile Replay Controller

Implement one behavioral Verilog-A source file named `file_profile_replay_controller.va`.

## Interface

Use this exact module interface:

```verilog
module file_profile_replay_controller (
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

Use $fseek(), $ftell(), and $rewind() together for profile replay bookkeeping.

Required behavior:

- open `stimulus_profile.txt` during `initial_step`;
- capture the starting file position with `$ftell`;
- read one line with `$fgets`;
- capture the new file position with `$ftell`;
- use `$fseek` to return to the starting position and read the first line again;
- call `$rewind` before closing the file;
- set `metric_v` to 1.0 when the second file position is greater than or equal to the first;
- on each rising `clk` crossing, reset state when `rst` is high;
- otherwise set `out_v` from the thresholded `V(vin)` value and add `0.01 * count_q` to `metric_v`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_profile_replay_controller.va`.
