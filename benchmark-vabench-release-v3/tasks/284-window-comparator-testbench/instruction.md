# Window Comparator Testbench

## Task Contract
Generate a Spectre transient testbench for the supplied window-comparator DUT. This is a testbench/support row: the DUT behavior is supplied, and the target artifact is the verification deck.

## Public Verilog-A Interface
The supplied support DUT declares `window_comparator_ref(VDD, VSS, vin, out)`. It drives `out` high only when `0.3 V < V(vin,VSS) < 0.6 V` and low otherwise.

## Public Parameter Contract
The generated deck should provide `VDD = 0.9 V` and `VSS = 0 V`, include `window_comparator_ref.va`, instantiate the DUT using instance-first/module-last Spectre syntax, run a transient analysis, and save scalar `vin` and `out` waveforms.

## Required Behavior
Drive `vin` with a PWL or triangular stimulus that covers all observable window regions: below the lower threshold, inside the window on a rising ramp, above the upper threshold, and inside the window again on a falling ramp. The transient should be long and fine enough to observe both window entries and exits cleanly.

## Modeling Constraints
Return a portable Spectre deck only. Do not modify or emit the supplied DUT, checker logic, waveform result files, out-of-band test hooks, or simulator side channels.

## Output Contract
Return exactly one file named `tb_window_comparator_ref.scs`.
