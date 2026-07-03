# Window Comparator Testbench

Generate a Spectre transient testbench for the supplied window-comparator DUT.

## Target Artifact

Return exactly one file named `tb_window_comparator_ref.scs`.

## Supplied DUT Contract

The supplied DUT declares `window_comparator_ref(VDD, VSS, vin, out)` and drives
`out` high only when `0.3 V < V(vin,VSS) < 0.6 V`.

## Testbench Contract

- Include `ahdl_include "window_comparator_ref.va"`.
- Provide `VDD = 0.9 V` and `VSS = 0 V`.
- Instantiate the DUT with instance-first/module-last Spectre syntax.
- Drive `vin` with a PWL or triangular waveform that visits below the window,
  inside the window on the rising ramp, above the window, and inside the window
  again on the falling ramp.
- Run `tran tran stop=90n maxstep=20p errpreset=conservative`.
- Save `vin` and `out` using plain scalar save names.

## Modeling Constraints

Return only `tb_window_comparator_ref.scs`. Do not modify or emit the supplied
DUT, checker logic, waveform result files, private test hooks, or
simulator-private side channels.
