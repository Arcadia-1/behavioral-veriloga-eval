# Update-Latched Mux4 Sampler

Implement a voltage-domain glitch-free 4:1 mux sampler with reset and update-qualified select latching.

## Public Interface

Declare module `clocked_mux4_sampler` with positional ports:

```verilog
module clocked_mux4_sampler(dsel0, dsel1, din0, din1, din2, din3,
                            update, rst, clks, dout);
```

All ports are scalar `electrical` voltage-domain ports.

## Functional Contract

- Treat `dsel0`, `dsel1`, `update`, `rst`, and `clks` as 0/0.9 V logic with a 0.45 V threshold.
- `rst` is active high. While reset is active, force the selected channel to `din0` and drive `dout` from `din0`.
- On each falling threshold crossing of `clks`, if reset is inactive and `update` is high, latch the current two-bit select code and sample the selected data input.
- If `update` is low on a falling clock edge, ignore changes on `dsel0/dsel1` and hold the previous sampled output.
- Use `dsel0` as the least significant select bit: `00 -> din0`, `01 -> din1`, `10 -> din2`, `11 -> din3`.
- Drive `dout` using smooth Verilog-A transitions from the sampled value.

## Output

Return exactly one source artifact named `clocked_mux4_sampler.va`. Do not generate a Spectre testbench.
