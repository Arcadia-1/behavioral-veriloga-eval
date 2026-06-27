# Window Comparator Testbench

Generate only `tb_window_comparator_ref.scs` for the supplied `window_comparator_ref.va` DUT.
This is a testbench-generation task: the exact stimulus, supply, save, and
transient settings below are part of the requested testbench artifact contract.
Do not modify or regenerate the supplied comparator DUT.

The DUT declares `window_comparator_ref(VDD, VSS, vin, out)` and drives `out` high only when `0.3 V < vin < 0.6 V`.

The testbench must include `ahdl_include "window_comparator_ref.va"`, provide `VDD = 0.9 V` and `VSS = 0 V`, instantiate the DUT with instance-first/module-last syntax, drive `vin` with a PWL or triangular waveform that visits below the window, inside the window on the rising ramp, above the window, and inside the window again on the falling ramp, run `tran tran stop=90n maxstep=20p errpreset=conservative`, and save `vin` and `out`.

Return only `tb_window_comparator_ref.scs`. Do not modify the support DUT.
