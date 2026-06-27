# Task 287 Audit

Absorbs v2 `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` into v3.
Existing v3 tasks 099/101/111 cover component/support slices; this task
preserves the composed measurement L2 flow.

- Useful scenario: pass as Measurement L2. Differential stimulus, dither, and fixed-gain measurement flows are useful verification/instrumentation building blocks.
- Reasonable task: pass. The public prompt fixes interfaces, required files, saved observables, and expected amplification behavior.
- Complete tests: pending fresh local recertification. The v2 checker/testbench and one concrete unity-gain negative are included; more near-miss flow negatives would strengthen final release evidence.
- Fair evaluation: pass in design. The hidden checker measures only public differential gain separation from saved public observables.

Classification note: this is not a Core Circuit L2 task. Its independent value is the measurement-flow composition and support harness behavior.
