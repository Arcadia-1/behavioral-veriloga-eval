# Dynamic Supply Level Driver

Implement one Verilog-A source file named `dynamic_supply_level_driver.va`.

## Public Interface

```verilog
module dynamic_supply_level_driver(din, vdd, vss, out);
```

All ports are electrical. `din` is a voltage-coded input, `vdd` and `vss` are
the local supply rails, and `out` is an electrical output driven relative to the
local rails.

## Public Parameter Contract

- `vsup_min = 0.55 V`: minimum `V(vdd, vss)` required for normal operation.
- `vth_frac = 0.5`: input threshold expressed as a fraction of the local supply
  range above `vss`.
- `vlo_frac = 0.0`, `vhi_frac = 1.0`: output low and high levels expressed as
  fractions of the local supply range above `vss`.
- `tr = 40p`: output transition smoothing time.

## Required Behavior

Model a dynamic-supply electrical level driver. Compute the input level relative
to the local rails, not global ground. When `V(vdd, vss)` is at least
`vsup_min`, drive `out` to the local low or high rail-derived level according to
whether the normalized input exceeds `vth_frac`. When the supply is below
`vsup_min`, drive `out` to the local low level. Smooth the output with
`transition()`.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not generate a testbench,
checker logic, connectmodule code, branch current contributions, transistor
devices, `ddt()`, or `idt()`. Do not hard-code visible or hidden stimulus times.
