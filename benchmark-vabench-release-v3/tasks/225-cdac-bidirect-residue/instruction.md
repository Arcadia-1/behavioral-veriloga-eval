# CDAC Bidirectional Residue

Implement the Verilog-A module `cdac_bidirect_residue` in `cdac_bidirect_residue.va`.

## Public Interface

Use the exact module interface:

```verilog
module cdac_bidirect_residue(vin, clks, dctrl1, dctrl2, dctrl3, dctrl4, dctrl5, dctrl6, dctrl7, vres);
input vin, clks, dctrl1, dctrl2, dctrl3, dctrl4, dctrl5, dctrl6, dctrl7;
output vres;
electrical vin, clks, dctrl1, dctrl2, dctrl3, dctrl4, dctrl5, dctrl6, dctrl7, vres;
```

## Required Behavior

Model a sampled capacitive DAC residue node for a SAR-style converter. On `initial_step` and on each falling transition of `clks` through mid-supply, sample `vin` into the residue state. When `dctrl7` falls, add the half-scale MSB residue step. When `dctrl6` through `dctrl1` rise, subtract binary-weighted residue steps from MSB toward LSB. The output `vres` must continuously drive the current residue state with a smooth voltage transition.

## Modeling Contract

Treat the digital control pins as voltage-domain logic inputs with a mid-supply threshold. Keep the model event-driven and voltage-domain; do not use transistor-level devices, current injection, hidden test hooks, or checker-specific side channels.
