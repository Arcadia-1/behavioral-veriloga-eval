# Agent-Visible Spec: vbr1_l1_window_comparator_detector:tb

One-shot testbench-generation task for a voltage-domain window comparator.

## Agent-Visible Input

- `window_comparator_ref.va`

## Required Output

- `tb_window_comparator_ref.scs`

## Public DUT Interface

The support DUT declares `window_comparator_ref(VDD, VSS, vin, out)`. It drives
`out` high when `vin` is inside the public `0.3 V < vin < 0.6 V` window and low
outside that window.

## Public Testbench Contract

The Spectre testbench must:

- include `ahdl_include "window_comparator_ref.va"`;
- provide `VDD = 0.9 V` and `VSS = 0 V`;
- instantiate `window_comparator_ref` with instance-first/module-last syntax;
- drive `vin` with a PWL or triangular waveform that visits below `0.3 V`,
  inside the `0.3 V` to `0.6 V` window, above `0.6 V`, and then returns
  through the window on the falling ramp;
- run `tran tran stop=90n maxstep=20p errpreset=conservative`;
- save `vin` and `out`.

`time` is the implicit transient waveform axis.

If the PWL `wave=[...]` array spans multiple physical lines, use Spectre
backslash line continuation, or keep the full array on one line.

## Functional Contract

The saved waveform should make the inside/outside behavior observable: `out`
should be high only while `vin` is inside the window and low outside it.

## Modeling Constraints

Return only the testbench. Do not modify or return the support DUT, add checker
logic, or use transistor-level devices, current-domain loads, AC/noise
analysis, or unsupported simulator features.
