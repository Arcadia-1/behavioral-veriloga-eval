# Analog Initial Block State

## Task Contract

Implement one Verilog-A source file named `analog_initial_block_state.va`. The task is an L0/support row for analog-initial state initialization in voltage-domain behavioral models.

This is a DUT task for Verilog-A language semantics. It is not a standalone AMS circuit macro.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module analog_initial_block_state(
    input electrical vin,
    output electrical out
);
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

Declare a real-valued state variable. Initialize that state to `0.25` in an `analog initial` block. In the main `analog` block, drive `out` as `V(vin) + initialized_state`.

## Modeling Constraints

Use the `analog initial` construct for initialization. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `analog_initial_block_state.va`.
