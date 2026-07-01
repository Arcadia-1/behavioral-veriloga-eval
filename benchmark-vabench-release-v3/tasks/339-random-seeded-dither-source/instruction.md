# Random Seeded Dither Source

Implement one behavioral Verilog-A DUT file named `random_seeded_dither_source.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module random_seeded_dither_source (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a deterministic seeded random function call, `$random(seed_q)`, inside the clocked behavior.

Use voltage-coded logic with `vth = 0.45` V and high outputs limited to `vhi = 0.9` V.

On `initial_step`, initialize an integer seed to `17`.

On every rising crossing of `clk`:

1. If `rst` is high, drive both `out` and `metric` low.
2. Otherwise call `$random(seed_q)` and convert the returned value to a non-negative integer.
3. Compute `code = random_value % 5`.
4. When `mode` is high, increment `code` by one.
5. Drive `metric = 0.1 * code`.
6. Drive `out = V(vin) + 0.05 * code`, clipped to `[0.0, vhi]`.

The evaluator samples the deterministic random sequence, the mode-dependent code offset, and reset clearing.

## Output

Return exactly one source artifact named `random_seeded_dither_source.va`. Do not generate a Spectre testbench for this task.
