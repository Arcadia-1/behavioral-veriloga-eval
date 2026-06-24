# Active High Reset Synchronizer

Implement `reset_sync_active_high.va` in Verilog-A.

## Interface

```verilog
module reset_sync_active_high(clk, rst, sync_rst);
```

Inputs: `clk, rst`.
Outputs: `sync_rst`.

## Required Behavior

Assert reset immediately when the asynchronous reset is asserted. On reset deassertion, release the synchronized reset only after two rising `clk` samples in the inactive state.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
