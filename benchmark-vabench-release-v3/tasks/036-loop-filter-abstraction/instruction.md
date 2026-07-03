# Sampled Loop-Filter Abstraction

Implement `loop_filter_abstraction.va` in Verilog-A.

## Interface

```verilog
module loop_filter_abstraction(
    input  electrical clk,
    input  electrical rst,
    input  electrical vin,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

This task asks for the `loop_filter_abstraction` behavioral DUT module, not a
Spectre testbench. The module is a sampled/event-driven PLL loop-filter
abstraction that approximates proportional and integral loop-control trends
without modeling a transistor-level or KCL/KVL RC network.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `tr` | `100 ps` | time, `(0:inf)` | Rise/fall smoothing for `out` and `metric`. |
| `deadband` | `0.05` | V, `[0:inf)` | Input-error magnitude below which loop updates hold state. |

Required observable behavior:

- Treat `clk` and `rst` as voltage-coded logic with a 0.45 V threshold.
- Interpret `vin` as a signed loop-error stimulus around 0.45 V.
- On each rising `clk` edge, update sampled loop-filter state when reset is
  low and `abs(V(vin) - 0.45)` exceeds `deadband`.
- Use a proportional correction whose step size decays across successive valid
  updates.
- Accumulate a smaller integral residual from the signed loop-error input.
- Drive `out` as a bounded loop-control voltage that responds upward for
  positive error and downward for negative error.
- Keep `out` bounded in the 0 V to 0.9 V range.
- Drive `metric` high only after several valid loop-filter updates and clear
  it on reset.
- When reset is high, clear the sampled state back near midscale and clear the
  update metric.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.
Use `transition(...)` for the driven output voltages.

## Output

Return exactly one source artifact named `loop_filter_abstraction.va`.
