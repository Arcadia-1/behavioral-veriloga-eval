# Limiter Rails

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive limiters
- Base function: Supply-referenced voltage limiter
- Domain: `voltage`
- Target artifact(s): `limiter_rails.va`
- Visible context: public task, module interface, port roles, and behavioral contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`limiter_rails.va` must declare:

```verilog
module limiter_rails(vdd, vss, vin, vmax, vmin, vout);
input vdd, vss, vin, vmax, vmin;
output vout;
electrical vdd, vss, vin, vmax, vmin, vout;
```

## Behavioral Contract

Implement a voltage limiter whose allowed output window is referenced to the supply rails:

- upper output limit: `V(vdd) - V(vmax)`
- lower output limit: `V(vss) + V(vmin)`

Pass `vin` when it is inside this window. Clamp to the corresponding limit when the input exceeds either bound.

Compute the limited target with real-valued behavioral logic, then drive `vout` with one voltage contribution. This keeps the model friendly to analog linting while preserving hard limiter behavior. Do not use current contributions, transistor devices, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `limiter_rails.va`.
Do not include explanatory prose outside the source artifact contents.
