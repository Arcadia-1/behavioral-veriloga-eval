# Limiter Rails

## Task Contract

Implement the requested Verilog-A artifact for `Limiter Rails`.
- Form: `dut`
- Level: `L1`
- Category: `mixed_signal`
- Target artifact(s): `limiter_rails.va`

- Base function: Supply-referenced voltage limiter
- Domain: `voltage`
- Output boundary: validation logic is external; do not generate validation harness or testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`limiter_rails.va` must declare:

```verilog
module limiter_rails(vdd, vss, vin, vmax, vmin, vout);
input vdd, vss, vin, vmax, vmin;
output vout;
electrical vdd, vss, vin, vmax, vmin, vout;
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

Implement a voltage limiter whose allowed output window is referenced to the supply rails:

- upper output limit: `V(vdd) - V(vmax)`
- lower output limit: `V(vss) + V(vmin)`

Pass `vin` when it is inside this window. Clamp to the corresponding limit when the input exceeds either bound.

Compute the limited target with real-valued behavioral logic, then drive `vout` with one voltage contribution. This keeps the model friendly to analog linting while preserving hard limiter behavior. Do not use current contributions, transistor devices, or testbench-specific constants.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `limiter_rails.va`.
Do not include explanatory prose outside the source artifact contents.
