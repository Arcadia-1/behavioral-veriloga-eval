# Converter Static Linearity Measurement

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Data Converter Measurement
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `converter_static_linearity_measurement_flow.va`
- Required module: `converter_static_linearity_measurement_flow`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Model a converter measurement-flow component, not just an ideal quantizer.

## Public Verilog-A Interface

```verilog
module converter_static_linearity_measurement_flow(clk, rst, vin, code, recon, dnl, inl);
```

All ports are electrical. `clk` is the sampling strobe, `rst` is an active-high
reset, `vin` is the swept converter input, and `code`, `recon`, `dnl`, and
`inl` are analog metric outputs.

## Public Parameter Contract

- `vth = 0.45 V`: threshold for voltage-coded clock and reset logic.
- `vfs = 0.9 V`: full-scale input range for the 4-bit converter sweep.
- `tr = 120p`: transition smoothing time for the metric outputs.

## Required Behavior

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

The public observable waveforms are `clk`, `rst`, `vin`, `code`, `recon`,
`dnl`, and `inl`.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A only. Do not emit a Spectre
testbench, checker, waveform sampler, current contribution, transistor-level
device, AC/noise analysis, `ddt()`, or `idt()`.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`converter_static_linearity_measurement_flow.va`. Do not include explanatory
prose outside the source artifact contents.
