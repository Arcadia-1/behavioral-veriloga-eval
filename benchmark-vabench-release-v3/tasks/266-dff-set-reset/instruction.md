# DFF Set Reset

## Task Contract

Implement `dff_set_reset.va` as a voltage-coded D flip-flop with active-low asynchronous set/reset and complementary outputs.

## Public Verilog-A Interface

Use this module signature:

```verilog
module dff_set_reset(setb, rstb, clk, vdd, gnd, d, q, qb);
```

All ports are scalar `electrical` nodes. `setb` and `rstb` are active-low asynchronous controls, `clk` is the sampling clock, `d` is the data input, `vdd`/`gnd` define the local rails, and `q`/`qb` are complementary outputs.

## Public Parameter Contract

- `td`: output transition delay, default `0`.
- `tr`: output rise/fall transition time, default `10p`.

## Required Behavior

- Initialize `q` low and `qb` high.
- Force `q` low when `rstb` is below the local rail midpoint.
- Force `q` high when `setb` is below the local rail midpoint.
- When both asynchronous controls are inactive, sample `d` on each rising `clk` crossing.
- Drive `qb` as the complement of `q`.
- Use the local `vdd` and `gnd` rails for output levels and thresholds.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A only. Do not add checker logic, out-of-band test hooks, simulator side channels, current contributions, `ddt()`, or `idt()`.

## Output Contract

Return exactly one source artifact named `dff_set_reset.va`.
