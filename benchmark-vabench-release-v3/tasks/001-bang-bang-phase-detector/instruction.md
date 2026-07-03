# Bang-Bang Phase Detector

Implement one Verilog-A DUT file named `bbpd_ref.va`.

The DUT is a bang-bang phase detector for a clock/data recovery loop. It compares the sampled relationship between the incoming data, the clock, and the retimed data, then emits short `up` or `down` correction pulses.

## Interface

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

Use voltage-domain `electrical` ports. Preserve the public parameters already present in the starter unless you have a specific reason to add compatible parameters.

## Required Behavior

Treat logic low as below `vth` and logic high as above `vth`; the starter uses `vth = 0.45` V and `vdd = 0.9` V.

On each rising or falling transition of `data`:

- assert `up` when `clk` is high and `retimed_data` is low;
- assert `down` when `clk` is low and `retimed_data` is high;
- assert neither output when the two inputs do not indicate a correction direction;
- never drive `up` and `down` high at the same time.

The correction output should be a voltage pulse near `vdd`, returning to 0 V after the next clock transition. Use smooth Verilog-A voltage contributions such as `transition(...)` for output drives.

## Public Smoke

The public smoke test instantiates the DUT, drives `data`, `clk`, and `retimed_data` pulse sources, and saves these scalar observables:

- `data`
- `clk`
- `retimed_data`
- `up`
- `down`

Additional verification may use broader deterministic stimulus to check
data-edge response, presence of both pulse directions, and non-overlap of `up`
and `down`.

## Output

Return exactly one source artifact named `bbpd_ref.va`. Do not generate a Spectre testbench for this task.
