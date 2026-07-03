# IQ Downconversion Chain

Implement `iq_downconversion_chain.va` in Verilog-A.

## Public Interface

```verilog
module iq_downconversion_chain(clk, rst, vin, out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon);
input clk, rst, vin;
output out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon;
electrical clk, rst, vin, out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon;
```

All ports are scalar electrical voltage-domain ports. `clk` is the quadrature
LO phase-advance clock and `rst` is an active-high voltage-coded reset. Use a
`0.45 V` logic threshold where a digital decision is needed.

## Public Parameter Contract

- `tr`: output transition smoothing time, default `80p`.
- `vth`: voltage-coded logic threshold, default `0.45`.

## Functional Contract

- Model a composed voltage-domain I/Q downconversion chain: quadrature LO
  sequencing, two mixer paths, bounded I/Q mixer monitors, and filtered
  baseband I/Q outputs.
- Treat `vin` as an RF-envelope voltage around `0.45 V` common mode.
- While reset is active, return the quadrature state and all analog observables
  to their reset/common-mode values.
- On each rising `clk` crossing after reset, advance a four-phase quadrature
  sequence. Expose the sequence through `phase_mon`.
- Drive `lo_i` and `lo_q` as voltage-coded I/Q LO polarity monitors for the
  current quadrature phase.
- Mix `V(vin) - 0.45` with the I and Q LO polarities to produce bounded
  `mix_i` and `mix_q` monitors.
- Drive `out` from the I-path baseband state and `metric` from the Q-path
  baseband state. When `vin` returns to common mode, both baseband states
  should settle back near common mode.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `iq_downconversion_chain.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, S-parameters, AC/noise analysis, `ddt()`, or `idt()`.
