# Directive Configurable Threshold

## Task Contract

Implement one behavioral Verilog-A DUT file named `directive_configurable_threshold.va`.

This task focuses on Verilog-A compiler-directive controlled threshold selection. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a sampled comparator whose default threshold is selected by a compile-time directive and then adjusted by a voltage-coded mode input.

## Public Verilog-A Interface

```verilog
module directive_configurable_threshold (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- Define `` `USE_HIGH_THRESHOLD`` as `1` in the source.
- Under `` `ifdef USE_HIGH_THRESHOLD``, declare `parameter real base_th = 0.60`.
- Under the `` `else`` branch, declare `parameter real base_th = 0.40`.
- Use `vth = 0.45` V for clock, mode, and reset decisions.
- Use high output level `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.

## Required Behavior

- Compute `eff_th = base_th - 0.10` when `V(mode) > vth`, otherwise `base_th`.
- On each rising crossing of `V(clk) - vth`, sample the comparator decision.
- If reset is high, clear both outputs to `0.0`.
- Otherwise drive `out = vhi` when `V(vin) > eff_th`, else `0.0`.
- Drive `metric = eff_th`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `directive_configurable_threshold.va`. Do not generate a Spectre testbench for this task.
