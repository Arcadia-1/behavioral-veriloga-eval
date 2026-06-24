# Lock Detector

Implement one Verilog-A DUT file named `lock_detector.va`.

The DUT is a voltage-domain reference/feedback lock detector for a PLL-style clock path. It observes rising edges on `ref_clk` and `fb_clk`, uses an active-low reset, and drives a scalar `lock` output.

## Interface

The file must define module `lock_detector` with this exact positional port order:

```verilog
module lock_detector(ref_clk, fb_clk, rst_n, lock);
    input ref_clk, fb_clk, rst_n;
    output lock;
    electrical ref_clk, fb_clk, rst_n, lock;
```

Use voltage-domain `electrical` ports. Treat logic low as below `vth` and logic high as above `vth`; the starter uses `vth = 0.45` V and `vdd = 0.9` V. Preserve compatible public parameters for `vth`, `vdd`, timing tolerance, required hit count, and output transition time.

## Required Behavior

- `rst_n` is active low. While reset is low, clear the consecutive-hit counter and drive `lock` low.
- On every rising edge of `fb_clk`, record that feedback edge time.
- Feedback edges observed while `rst_n` is low must not count toward a later post-reset lock sequence.
- On every rising edge of `ref_clk` while reset is high, compare the reference edge time with the most recent feedback rising edge time.
- A reference event is aligned only when the most recent feedback rising edge is within `2 ns` of that reference rising edge.
- Assert `lock` only after three consecutive aligned reference events.
- Before the third consecutive aligned reference event, `lock` must remain low.
- Any reference event whose most recent feedback edge is outside the `2 ns` window breaks the streak and drives `lock` low.
- A later active-low reset must clear an already asserted lock and require three new consecutive aligned reference events before reassertion.

Use voltage contributions for `lock`, preferably with `transition(...)`. Do not use current contributions, `ddt()`, or `idt()`.

## Public Smoke

The public smoke test instantiates the DUT and saves these scalar observables:

- `ref_clk`
- `fb_clk`
- `rst_n`
- `lock`

The hidden evaluator uses deterministic broader SCS stimulus to check reset behavior, no early lock, three aligned rising-edge lock acquisition, and mismatch-induced streak breaking.

## Output

Return exactly one source artifact named `lock_detector.va`. Do not generate a Spectre testbench for this task.
