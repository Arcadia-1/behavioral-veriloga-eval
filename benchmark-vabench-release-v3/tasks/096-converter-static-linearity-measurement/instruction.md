# Converter Static Linearity Measurement

Implement one Verilog-A source file named
`converter_static_linearity_measurement_flow.va`.

## Public Interface

```verilog
module converter_static_linearity_measurement_flow(clk, rst, vin, code, recon, dnl, inl);
```

All ports are electrical. `clk` is the sampling strobe, `rst` is an
active-high reset, `vin` is the swept converter input, and `code`, `recon`,
`dnl`, and `inl` are analog metric outputs.

## Public Parameter Contract

- `vth = 0.45 V`: threshold for voltage-coded clock and reset logic.
- `vfs = 0.9 V`: full-scale input range for the 4-bit converter sweep.
- `tr = 120p`: transition smoothing time for the metric outputs.

## Required Behavior

This is an L2 converter measurement-flow component, not just an ideal quantizer.
On each rising crossing of `clk`, reset the retained state when `rst` is high.
Otherwise, clip `vin` to the 0-to-`vfs` range, quantize it to a 4-bit code, and
drive `code` as the code index times `vfs / 15`.

Drive `recon` as a monotonic but deliberately non-ideal DAC reconstruction of
the current code. The reconstruction should have visibly non-uniform step sizes
so that DNL-like behavior can be observed from the waveform history.

Drive `inl` as a bounded analog metric centered near 0.45 V that reflects the
current reconstruction error relative to an ideal `vfs / 15` ramp. Drive `dnl`
as a bounded analog metric centered near 0.45 V that reflects the most recent
positive code-step error relative to the ideal step size; when there is no prior
valid increasing code step, return the DNL metric to its common-mode value.

## Public Verification Context

The public transient scenario saves `clk`, `rst`, `vin`, `code`, `recon`, `dnl`,
and `inl` over a 96 ns converter sweep. Treat those values as the verification
scenario for observable behavior, not as private checker implementation details.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A only. Do not emit a Spectre
testbench, checker logic, private waveform sample points, current
contributions, transistor-level devices, AC/noise analysis, `ddt()`, or
`idt()`.
