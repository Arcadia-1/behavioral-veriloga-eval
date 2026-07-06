# Voltage-Coded DFF With Reset

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Voltage-Coded Logic Support
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `source_dff_reset.va`
- Required module: `source_dff_reset`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Model a voltage-coded D flip-flop with explicit reset behavior for AMS control paths.

## Public Verilog-A Interface

`source_dff_reset.va` declares module `source_dff_reset` with positional ports:

```verilog
module source_dff_reset(vin_d, vclk, rst, vout_q, vout_qbar);
```

All ports are electrical. `vin_d` is the voltage-coded data input, `vclk` is the
sampling clock, `rst` is the reset input, and `vout_q` and `vout_qbar` are
voltage-coded outputs.

## Public Parameter Contract

- `vlogic_high = 0.9 V`: output level for logic 1.
- `vlogic_low = 0.0 V`: output level for logic 0.
- `vtrans_clk = 0.45 V`: rising-clock and reset threshold.
- `vtrans = 0.45 V`: data input decision threshold.
- `tdel = 500p`: output propagation delay.
- `trise = 20p`: output rising transition time.
- `tfall = 20p`: output falling transition time.

## Required Behavior

On each rising crossing of `vclk` through `vtrans_clk`, sample `vin_d` using
`vtrans` and drive `vout_q` to the sampled logic value while driving
`vout_qbar` to its complement. On each rising crossing of `rst` through
`vtrans_clk`, force both outputs low. Hold the most recent state between clock
and reset events.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A and smoothed voltage contributions
only. Do not use current contributions, transistor-level devices, `ddt()`,
`idt()`, checker logic, or testbench-specific sample times.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`source_dff_reset.va`. Do not include explanatory prose outside the source
artifact contents.
