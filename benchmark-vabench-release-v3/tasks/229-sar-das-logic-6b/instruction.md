# 6-bit SAR DAS Logic

Implement the Verilog-A module `sar_das_logic_6b` in `sar_das_logic_6b.va`.

## Public Interface

Use the exact module interface:

```verilog
module sar_das_logic_6b(clk_sampling, clk_sar, vcomp, d1, d2, d3, d4, d5, d6, db1, db2, db3, db4, db5, db6, co, cob);
input clk_sampling, clk_sar, vcomp;
output d1, d2, d3, d4, d5, d6, db1, db2, db3, db4, db5, db6, co, cob;
electrical clk_sampling, clk_sar, vcomp, d1, d2, d3, d4, d5, d6, db1, db2, db3, db4, db5, db6, co, cob;
```

Public parameters should include `vdd=1.1`, `vcm=0.55`, and edge/output timing parameters for smooth voltage transitions.

## Required Behavior

Model the differential bit-control logic used around a 6-bit SAR conversion. A rising `clk_sampling` transition clears all `d*`, `db*`, `co`, and `cob` outputs and resets the internal bit pointer. A falling `clk_sampling` transition presets all differential bit controls high while keeping `co/cob` low. Each rising `clk_sar` transition compares `vcomp` against `vcm`, emits a one-cycle `co` or `cob` decision pulse, and updates the next differential bit-control pair in MSB-to-LSB order. Each falling `clk_sar` transition clears `co/cob` back low.

## Modeling Contract

Drive logic-high outputs to `vdd` and logic-low outputs to ground-equivalent voltage using smooth transitions. Keep the model event-driven and voltage-domain; do not use transistor-level devices, current injection, hidden test hooks, or checker-specific side channels.
