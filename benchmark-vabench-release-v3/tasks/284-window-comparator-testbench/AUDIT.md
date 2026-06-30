# Task 284 Audit

Absorbs v2 `vbr1_l1_window_comparator_detector:tb` into v3.

- Useful scenario: pass. Testbench generation for a threshold/window detector is a practical verification task.
- Reasonable task: pass. The DUT is supplied and the required waveform coverage and saved observables are public.
- Complete tests: pending fresh local recertification. Hidden checker and gold testbench are imported from v2; one concrete negative removes the window sweep.
- Fair evaluation: pass in design. The checker evaluates only public `vin/out` behavior required by the prompt.
