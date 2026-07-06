# VCO Phase Integrator

## Task Contract

Implement the requested Verilog-A artifact for `VCO Phase Integrator`.
- Form: `dut`
- Level: `L1`
- Category: `pll_clock_timing`
- Target artifact(s): `vco_phase_integrator.va`

Implement `vco_phase_integrator.va` in Verilog-A.

## Public Verilog-A Interface

```verilog
module vco_phase_integrator(
    input  electrical vctrl,
    output electrical phase,
    output electrical clk
);
```

## Public Parameter Contract

Provide this overrideable public parameter:

| Parameter | Default | Unit / Range | Contract |
| --- | ---: | --- | --- |
| `tr` | `200 ps` | time, `(0:inf)` | Rise/fall smoothing for `phase` and `clk`. |

## Required Behavior

The module is a voltage-controlled oscillator phase accumulator that exposes both wrapped phase and a voltage-coded clock.

- Maintain a real phase state normalized to the range `[0, 1)`.
- Update the phase state on a periodic 1 ns timer.
- At each update, increment phase by `0.03 + 0.09 * V(vctrl)`.
- When the phase reaches or exceeds 1.0, wrap it by one cycle and toggle
  `clk`.
- Drive `phase` as the wrapped normalized phase voltage.
- Drive `clk` as a smoothed 0 V / 0.9 V voltage-coded clock.
- Later clock-edge rate should increase when `vctrl` is higher than earlier
  `vctrl`.

## Modeling Constraints

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, validation logic, validation-only
test hooks, or simulator-specific side channels.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `vco_phase_integrator.va`.
