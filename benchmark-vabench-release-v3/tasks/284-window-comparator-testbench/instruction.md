# Window Comparator Testbench

Generate `tb_window_comparator_ref.scs` for the supplied
`window_comparator_ref.va` DUT.

## Supplied DUT

The supplied DUT declares `window_comparator_ref(VDD, VSS, vin, out)` and
drives `out` high only when `0.3 V < vin < 0.6 V`.

## Testbench Contract

- Include `ahdl_include "window_comparator_ref.va"`.
- Provide `VDD = 0.9 V` and `VSS = 0 V`.
- Instantiate the DUT with instance-first/module-last Spectre syntax.
- Drive `vin` with a PWL or triangular waveform that visits below the window,
  inside the window on the rising ramp, above the window, and inside the window
  again on the falling ramp.
- Run `tran tran stop=90n maxstep=20p errpreset=conservative`.
- Save `vin` and `out`.

## Modeling Constraints

Return only `tb_window_comparator_ref.scs`. Do not modify or emit the supplied
DUT, checker logic, private test hooks, waveform files, or simulator-private
side channels.
