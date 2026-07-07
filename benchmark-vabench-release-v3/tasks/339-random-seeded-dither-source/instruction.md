# Random Seeded Dither Source

## Task Contract

Implement one behavioral Verilog-A DUT file named `random_seeded_dither_source.va`.

This task focuses on clocked seeded-random dither generation with `$random(seed)`. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a clocked dither source that derives a small discrete dither code from a deterministic seeded Verilog-A random call.

## Public Verilog-A Interface

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

## Public Parameter Contract

- Use `vth = 0.45` V.
- Use high output level limit `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- On `initial_step`, initialize an integer seed state to `17`.
- Use `$random(seed_q)` inside the clocked event body; do not replace it with a fixed pattern.

## Required Behavior

- On each rising crossing of `V(clk) - vth`, update both outputs.
- If reset is high, clear both outputs to `0.0`.
- Otherwise call `$random(seed_q)` and convert the returned value to a non-negative integer code source.
- Compute `code = random_value % 5`.
- When mode is high, increment `code` by one.
- Drive `metric = 0.1 * code`.
- Drive `out = V(vin) + 0.05 * code`, clipped to `0.0 ... vhi`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `random_seeded_dither_source.va`. Do not generate a Spectre testbench for this task.
