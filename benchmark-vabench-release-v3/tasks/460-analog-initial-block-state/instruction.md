# Analog Initial Block State

Implement one Verilog-A source file named `analog_initial_block_state.va`.

## Required Feature

Use an analog initial block to initialize behavioral state.

## Required Interface

```verilog
module analog_initial_block_state(
    input electrical vin,
    output electrical out
);
```

## Required Behavior

- Declare a real-valued state variable.
- In an `analog initial` block, initialize that state variable to exactly `0.25`.
- In the main `analog` block, drive `out` as `V(vin) + initialized_state`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `analog_initial_block_state.va`.
