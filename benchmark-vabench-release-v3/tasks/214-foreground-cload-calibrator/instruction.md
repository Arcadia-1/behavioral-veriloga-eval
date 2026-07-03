# Foreground Cload Calibrator

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, Trim, and DEM Control
- Base function: foreground capacitor-load calibration controller
- Domain: `voltage`
- Target artifact(s): `foreground_cload_calibrator.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `foreground_cload_calibrator.va`.
- Preserve the public module name, positional port order, electrical disciplines, and output bit order.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `foreground_cload_calibrator` with positional ports:

```verilog
module foreground_cload_calibrator(ck, d, vrefp, vrefn,
    dcp0, dcp1, dcp2, dcp3, dcp4,
    dcn0, dcn1, dcn2, dcn3, dcn4,
    cvinp, cvinn, en, enb);
```

All ports are electrical. `ck` is the calibration capture clock, `d` is the
comparator decision input, `vrefp/vrefn` are reference inputs passed to the
calibration stimulus outputs, `dcp0..dcp4` and `dcn0..dcn4` are complementary
capacitor-load trim bits, and `en/enb` indicate whether foreground calibration
is still active.

## Public Parameter Contract

Provide overrideable parameter `vdd = 1.0 V`. Treat voltage-coded decisions
with threshold `0.5*vdd`. Drive active digital outputs near `vdd` and inactive
outputs near `0 V`.

## Required Behavior

Initialize calibration as active. On each rising crossing of `ck`, while the
capture phase is active, sample `d` and capture one complementary trim decision
from bit 4 down to bit 0. A low decision sets the corresponding `dcp` bit high
and `dcn` bit low; a high decision sets the corresponding `dcn` bit high and
`dcp` bit low. After the five-bit capture phase completes, deassert `en` and
assert `enb`. Continuously drive `cvinp` from `vrefp` and `cvinn` from `vrefn`.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth discrete voltage outputs with `transition(...)`. Do not
add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, transistor-level
devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.

## Output Contract

Return exactly one complete Verilog-A file named `foreground_cload_calibrator.va`.
Do not include explanatory prose outside the source artifact contents.
