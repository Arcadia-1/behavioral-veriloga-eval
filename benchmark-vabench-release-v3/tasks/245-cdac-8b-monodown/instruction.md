# Source CDAC 8b Monodown

Implement an 8-bit SAR CDAC residue model. On CLKS falling, sample VIN into VRES; on DCTRL7..DCTRL1 rising, subtract binary-weighted fractions from the held residue.

The module name and port list must match `cdac_8b_monodown.va`. Keep the model voltage-domain only and deterministic. The historical source normalized for this task is `liudongyang/L2_cdac_8b_ideal.va`.
