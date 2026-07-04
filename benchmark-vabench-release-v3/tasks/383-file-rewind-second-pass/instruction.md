# File Rewind Second Pass

## Task Contract

Implement one behavioral Verilog-A DUT source file named `file_rewind_second_pass.va`. The DUT uses the supplied `config_lines.txt` support artifact to prove that an opened file can be read, rewound, and read again before driving a clocked threshold output.

## Form-Specific Requirements

This is a DUT task. Keep the provided module name and port list, read the public support file at runtime, and do not generate a testbench or auxiliary artifacts. Keep the model voltage-domain behavioral and do not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module file_rewind_second_pass (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

The `mode` port is present for interface consistency and is not part of the file-rewind decision.

## Public Parameter Contract

Use `vth = 0.45` as the analog logic threshold, `vhi = 0.9` as the high output and metric level, and `tr = 200p` as the transition rise/fall time. These parameters may be overridden by the testbench and should be used consistently for thresholding, output level, and transitions.

The support file `config_lines.txt` is public. It contains a gain key/value row followed by a mode key/value row. Ordinary line terminators from `$fgets` must not prevent parsing the key/value content.

## Required Behavior

During `initial_step`, open `config_lines.txt`, read the first two lines with `$fgets`, call `$rewind(fd)`, read the first line again, and close the file. Treat the rewind qualification as successful only when the first pass observes gain `0.8` then mode `1`, and the second pass again observes gain `0.8`.

Set `metric` high when that rewind qualification succeeds, otherwise low. On each rising crossing of `clk`, reset `out` low when `rst` is above `vth`; otherwise drive `out` high only when the rewind qualification succeeded and `vin` is above `vth`.

## Modeling Constraints

Use `$fopen`, `$fgets`, `$rewind`, `$fclose`, `cross`, and `transition`. Parse the loaded text content rather than comparing against strings that include simulator-dependent line terminators. Do not hard-code behavior from a testbench waveform.

## Output Contract

Return exactly one source artifact named `file_rewind_second_pass.va`. Drive both `out` and `metric` with `transition(...)`.
