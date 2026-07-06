# Bang-Bang Phase Detector

## Task Contract

Implement the requested Verilog-A artifact for `Bang Bang Phase Detector`.
- Form: `dut`
- Level: `L1`
- Category: `pll_clock_timing`
- Target artifact(s): `bbpd_ref.va`

Implement one Verilog-A DUT file named `bbpd_ref.va`.

The DUT is a bang-bang phase detector for a clock/data recovery loop. It compares the sampled relationship between the incoming data, the clock, and the retimed data, then emits short `up` or `down` correction pulses.

## Public Verilog-A Interface

The file must define module `bbpd_ref` with this exact positional port order:

```verilog
module bbpd_ref (
    input  electrical data,
    input  electrical clk,
    input  electrical retimed_data,
    output electrical up,
    output electrical down
);
```

Use voltage-domain `electrical` ports.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: voltage-coded logic high level for `up` and `down`.
- `vth = 0.45 V`: logic threshold for `data`, `clk`, and `retimed_data`.
- `trf = 10 ps`: rise/fall smoothing time for correction pulses.
- `td = 0 ps`: output transition delay.

## Required Behavior

Treat logic low as below `vth` and logic high as above `vth`.

On each rising or falling transition of `data`:

- assert `up` when `clk` is high and `retimed_data` is low;
- assert `down` when `clk` is low and `retimed_data` is high;
- assert neither output when the two inputs do not indicate a correction direction;
- never drive `up` and `down` high at the same time.

The correction output should be a voltage pulse near `vdd`, returning to 0 V after the next clock transition. Use smooth Verilog-A voltage contributions such as `transition(...)` for output drives.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `bbpd_ref.va`. Do not generate a Spectre testbench for this task.
