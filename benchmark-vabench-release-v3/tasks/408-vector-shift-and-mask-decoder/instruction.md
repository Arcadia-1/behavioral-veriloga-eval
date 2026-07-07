# Vector Shift And Mask Decoder

## Task Contract

Implement one behavioral Verilog-A source file named `vector_shift_and_mask_decoder.va`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module vector_shift_and_mask_decoder (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use shifts and masks for compact code decoding.

Required behavior:

- initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and state when `rst > vth`;
- otherwise set `code_q = count_q + 12`;
- set `field_q = (code_q >> 1) & 3`;
- set `out_v = (field_q == 2) ? vhi : 0.0`;
- set `metric_v = field_q`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `vector_shift_and_mask_decoder.va`.
