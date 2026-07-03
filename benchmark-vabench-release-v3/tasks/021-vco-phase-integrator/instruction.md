# VCO Phase Integrator

Implement `vco_phase_integrator.va` in Verilog-A.

## Interface

```verilog
module vco_phase_integrator(
    input  electrical vctrl,
    output electrical phase,
    output electrical clk
);
```

## Required Behavior

This task asks for the `vco_phase_integrator` behavioral DUT module, not a
Spectre testbench. The module is a voltage-controlled oscillator phase
accumulator that exposes both wrapped phase and a voltage-coded clock.

Support this public parameter and legal override:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `tr` | `200 ps` | time, `(0:inf)` | Rise/fall smoothing for `phase` and `clk`. |

Required observable behavior:

- Maintain a real phase state normalized to the range `[0, 1)`.
- Update the phase state on a periodic 1 ns timer.
- At each update, increment phase by `0.03 + 0.09 * V(vctrl)`.
- When the phase reaches or exceeds 1.0, wrap it by one cycle and toggle
  `clk`.
- Drive `phase` as the wrapped normalized phase voltage.
- Drive `clk` as a smoothed 0 V / 0.9 V voltage-coded clock.
- Later clock-edge rate should increase when `vctrl` is higher than earlier
  `vctrl`.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `vco_phase_integrator.va`.
