# Foreground Cload Calibrator

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: calibration/trim control.
- Target artifact: `foreground_cload_calibrator.va`.
- Role: foreground capacitor-load trim controller.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module foreground_cload_calibrator(ck, d, vrefp, vrefn, dcp0, dcp1, dcp2, dcp3, dcp4, dcn0, dcn1, dcn2, dcn3, dcn4, cvinp, cvinn, en, enb);
```

`ck` is the calibration clock, `d` is the comparator decision input, `vrefp/vrefn` are forwarded stimulus references, `dcp0..dcp4` and `dcn0..dcn4` are complementary trim bits, and `en/enb` report calibration activity. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameter `vdd = 1.0`. Use `0.5*vdd` as the clock and decision threshold and 0/`vdd` as the digital output levels.

## Required Behavior

Initialize calibration active with all trim bits low. On each rising `ck` crossing while the five-bit capture phase is active, sample `d` and capture one complementary trim decision from bit 4 down to bit 0. A low decision sets the matching `dcp` bit high and `dcn` bit low; a high decision sets `dcn` high and `dcp` low. After the capture phase completes, deassert `en` and assert `enb`. Continuously drive `cvinp` from `vrefp` and `cvinn` from `vrefn`.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `foreground_cload_calibrator.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
