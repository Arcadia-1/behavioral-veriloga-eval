# Sampled Loop-Filter Abstraction

## Task Contract

Implement the requested Verilog-A artifact for `Loop Filter Abstraction`.
- Form: `dut`
- Level: `L1`
- Category: `pll_clock_timing`
- Target artifact(s): `loop_filter_abstraction.va`

Implement `loop_filter_abstraction.va` in Verilog-A.

## Public Verilog-A Interface

```verilog
module loop_filter_abstraction(
    input  electrical clk,
    input  electrical rst,
    input  electrical vin,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Provide these overrideable public parameters:

| Parameter | Default | Unit / Range | Contract |
| --- | ---: | --- | --- |
| `tr` | `100 ps` | time, `(0:inf)` | Rise/fall smoothing for `out` and `metric`. |
| `deadband` | `0.05` | V, `[0:inf)` | Input-error magnitude below which loop updates hold state. |

## Required Behavior

The module is a sampled/event-driven PLL loop-filter abstraction that approximates proportional and integral loop-control trends without modeling a transistor-level or KCL/KVL RC network.

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

## Modeling Constraints

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, validation logic, validation-only
test hooks, or simulator-specific side channels. Use `transition(...)` for the
driven output voltages.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `loop_filter_abstraction.va`.
