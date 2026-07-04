# Foreground RDAC Calibrator

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, Trim, and DEM Control
- Base function: foreground RDAC calibration controller
- Domain: `voltage`
- Target artifact(s): `foreground_rdac_calibrator.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `foreground_rdac_calibrator.va`.
- Preserve the public module name, positional port order, electrical disciplines, and output bit order.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `foreground_rdac_calibrator` with positional ports:

```verilog
module foreground_rdac_calibrator(ck, d, vrefp, vrefn,
    dc0, dc1, dc2, dc3, dc4, dc5, dc6,
    cvinp, cvinn, en, enb);
```

All ports are electrical. `ck` is the calibration update clock, `d` is the
comparator decision input, `vrefp/vrefn` are reference inputs passed to
`cvinp/cvinn`, `dc0..dc6` are the voltage-coded RDAC control bits, and
`en/enb` indicate whether foreground calibration is still active.

## Public Parameter Contract

Provide overrideable parameter `vdd = 1.0 V`. Treat voltage-coded decisions
with threshold `0.5*vdd`. Drive active digital outputs near `vdd` and inactive
outputs near `0 V`.

## Required Behavior

Initialize calibration as active with the most-significant RDAC trial bit set.
On rising crossings of `ck`, walk the trial from bit 6 down to bit 0. A low
decision keeps the current trial bit and enables the next lower trial bit. A
high decision clears the current trial bit before enabling the next lower trial
bit. After the low-bit trial window completes, deassert `en` and assert `enb`.
Continuously drive `cvinp` from `vrefp` and `cvinn` from `vrefn`.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth discrete voltage outputs with `transition(...)`. Do not
add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, transistor-level
devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.

## Output Contract

Return exactly one complete Verilog-A file named `foreground_rdac_calibrator.va`.
Do not include explanatory prose outside the source artifact contents.
