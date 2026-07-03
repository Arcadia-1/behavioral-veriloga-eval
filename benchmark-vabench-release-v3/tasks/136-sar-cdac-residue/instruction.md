Implement a scalar-port version of a 7-bit SAR CDAC residue model.

The module must be named `sar_cdac_residue` and use this port order:

`VIN, CLK, S6, S5, S4, S3, S2, S1, VRES`

Sample `VIN` on `initial_step` and on rising `CLK`. Then adjust the residue on
control crossings: `S6` falling adds 1/2 full-scale, while rising `S5`..`S1`
subtract 1/4, 1/8, 1/16, 1/32, and 1/64 full-scale respectively.
