# Foreground RDAC Calibrator

Implement a voltage-domain foreground RDAC calibration controller.

## Public Interface

Return exactly one Verilog-A source file named `foreground_rdac_calibrator.va`.
Declare module `foreground_rdac_calibrator` with positional ports `ck, d,
vrefp, vrefn, dc0, dc1, dc2, dc3, dc4, dc5, dc6, cvinp, cvinn, en, enb`. All
ports are electrical.

`ck` is the calibration update clock, `d` is the comparator decision input,
`vrefp/vrefn` are reference inputs passed to `cvinp/cvinn`, `dc0..dc6` are the
voltage-coded RDAC control bits, and `en/enb` indicate whether foreground
calibration is still active.

## Public Parameter Contract

Provide overrideable parameter `vdd = 1.0 V`. Treat voltage-coded decisions
with threshold `0.5*vdd`. Drive active digital outputs near `vdd` and inactive
outputs near `0 V`.

## Functional Contract

Initialize calibration as active with the most-significant RDAC trial bit set.
On rising crossings of `ck`, walk the trial from bit 6 down to bit 0. A low
decision keeps the current trial bit and enables the next lower trial bit. A
high decision clears the current trial bit before enabling the next lower trial
bit. After the low-bit trial window completes, deassert `en` and assert `enb`.
Continuously drive `cvinp` from `vrefp` and `cvinn` from `vrefn`.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth discrete voltage outputs with `transition(...)`. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis
behavior.
