# Directive Configurable Threshold

Implement one behavioral Verilog-A DUT file named `directive_configurable_threshold.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use compiler directives to select the default threshold used by a clocked comparator.

This is a pure voltage-domain behavioral task. Do not use current-domain `I(...)` branch contributions.

Use voltage-coded logic with high outputs near `0.9` V.

Implement:

- define ``USE_HIGH_THRESHOLD`` as ``1`` in the source
- under `` `ifdef USE_HIGH_THRESHOLD``, declare `parameter real base_th = 0.60`
- under the `` `else`` branch, declare `parameter real base_th = 0.40`
- compute `eff_th = base_th - 0.10` when `V(mode) > 0.45`, otherwise `base_th`
- on each rising crossing of `V(clk) - 0.45`, sample the comparison
- if `V(rst) > 0.45`, clear both outputs to `0.0`
- otherwise drive `out = 0.9` when `V(vin) > eff_th`, else `0.0`
- drive `metric = eff_th`

The hidden testbench drives `vin = 0.55` and toggles `mode`. With the high-threshold compile path, the first clock sample must stay low at threshold `0.60`, while the later mode-enabled sample must go high at threshold `0.50`.

## Output

Return exactly one source artifact named `directive_configurable_threshold.va`. Do not generate a Spectre testbench for this task.
