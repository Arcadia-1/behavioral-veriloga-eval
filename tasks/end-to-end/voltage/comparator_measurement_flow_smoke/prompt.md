# Single-ramp comparator offset measurement flow smoke test

Write a pure voltage-domain Verilog-A single-ramp comparator offset measurement flow and its Spectre transient testbench.

Return exactly these source artifacts:

- `comparator_offset_search_ref.va`
- `tb_comparator_offset_search_ref.scs`

The Verilog-A module must be named `comparator_offset_search_ref` and use these positional ports:

`vdd`, `vss`, `inp`, `inn`, `outp`, `trip_v`, `offset_est`, `valid`

Requirements:

1. Use electrical ports and include `constants.vams` and `disciplines.vams`.
2. Implement a comparator with built-in static offset `vos = 5m`.
3. Drive `outp` high when `V(inp, vss) - V(inn, vss) > vos`.
4. On the rising threshold crossing, latch `trip_v = V(inp, vss)` and `offset_est = V(inp, vss) - V(inn, vss)`.
5. Drive `valid` low before the first rising crossing and high after the measurement latches.
6. Keep `trip_v` and `offset_est` stable after `valid` goes high.
7. Use EVAS-compatible `@(initial_step)`, directional `cross()` events, and `transition()`.
8. The testbench must set `vdd = 0.9 V`, `vss = 0 V`, `inn = 0.500 V`, perform a single ramp of `inp` from 0.490 V to 0.520 V, run `tran` to 100 ns, and save `inp`, `inn`, `outp`, `trip_v`, `offset_est`, and `valid`.

Avoid transistor-level devices, current-domain checks, AC/noise analysis, `ddt()`, and `idt()`.
