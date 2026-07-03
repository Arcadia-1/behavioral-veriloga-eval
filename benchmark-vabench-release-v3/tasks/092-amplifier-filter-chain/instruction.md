# Amplifier Filter Chain

Implement `amplifier_filter_chain.va` in Verilog-A.

## Public Interface

```verilog
module amplifier_filter_chain(clk, rst, vin, out, metric, preamp_mon, filt1_mon, filt2_mon, settle_metric);
```

Declare `clk`, `rst`, and `vin` as inputs and `out`, `metric`,
`preamp_mon`, `filt1_mon`, `filt2_mon`, and `settle_metric` as outputs. All
ports are scalar electrical voltage-domain ports. `clk` and `rst` are
voltage-coded logic signals with a `0.45 V` threshold.

## Public Parameter Contract

- `tr`: output transition smoothing time, default `100p`.
- `gain`: pre-filter gain around the `0.45 V` common-mode level, default `1.8`.
- `alpha`: sampled low-pass update coefficient for each cascaded filter state,
  default `0.30`.

## Functional Contract

- Implement a composed baseband conditioning block: a bounded gain stage
  followed by two cascaded sampled low-pass states.
- Initialize the pre-filter target, both filter states, `out`, `metric`,
  `preamp_mon`, `filt1_mon`, and `filt2_mon` near `0.45 V`; initialize
  `settle_metric` low.
- On each rising `clk` crossing, update the chain. While `rst` is active high,
  reset the chain to the initial common-mode state.
- When reset is low, form a pre-filter target by amplifying `vin` around
  `0.45 V` and bounding the target to the signal rails.
- Drive `metric` and `preamp_mon` from the bounded pre-filter target.
- Drive `filt1_mon` and `filt2_mon` from the two cascaded low-pass states.
- Drive `out` from the second filtered state so it visibly lags the pre-filter
  target during large input changes.
- Drive `settle_metric` as a voltage-coded settled-status output: high when
  the filtered output is close to the pre-filter target, low while the chain is
  still recovering.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `amplifier_filter_chain.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, AC/noise analysis, `ddt()`, or `idt()`.
