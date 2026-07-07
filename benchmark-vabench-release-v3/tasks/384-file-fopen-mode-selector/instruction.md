# File Fopen Mode Selector

## Task Contract

Implement one behavioral Verilog-A DUT source file named `file_fopen_mode_selector.va`. The DUT explicitly opens the supplied `config_lines.txt` support artifact in read mode, parses the first configuration row, and uses that result to qualify a clocked threshold output.

This is a DUT task. Keep the provided module name and port list, read the public support file at runtime, and do not generate a testbench or auxiliary artifacts. Keep the model voltage-domain behavioral and do not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module file_fopen_mode_selector (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

The `mode` port is present for interface consistency and is not part of the file-open decision.

## Public Parameter Contract

Use `vth = 0.45` as the analog logic threshold, `vhi = 0.9` as the high output and metric level, and `tr = 200p` as the transition rise/fall time. These parameters may be overridden by the testbench and should be used consistently for thresholding, output level, and transitions.

The support file `config_lines.txt` is public. Its first line is a gain key/value row. Ordinary line terminators from `$fgets` must not prevent parsing the key/value content.

## Required Behavior

During `initial_step`, open `config_lines.txt` with explicit read mode `"r"`, read the first line with `$fgets`, and close the file. Treat the open/read qualification as successful when the loaded key/value content indicates gain `0.8`.

Set `metric` high when that open/read qualification succeeds, otherwise low. On each rising crossing of `clk`, reset `out` low when `rst` is above `vth`; otherwise drive `out` high only when the open/read qualification succeeded and `vin` is above `vth`.

## Modeling Constraints

Use `$fopen`, `$fgets`, `$fclose`, `cross`, and `transition`. Parse the loaded text content rather than comparing against a string that includes simulator-dependent line terminators. Do not hard-code behavior from a testbench waveform.

## Output Contract

Return exactly one source artifact named `file_fopen_mode_selector.va`. Drive both `out` and `metric` with `transition(...)`.
