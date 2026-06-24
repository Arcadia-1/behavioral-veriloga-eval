# SOP Audit: Deterministic Jittered Clock Source

- Useful scenario: testbench utility module for behavioral Verilog-A validation flows.
- Reasonable task: public prompt states the scored interface and deterministic behavior.
- Complete tests: visible smoke plus hidden EVAS/Spectre-compatible transient testbench.
- Fair evaluation: hidden checker derives expected behavior from the public contract and concrete negative variants are expected to compile but fail correctness.

Certification status: certified with EVAS gold PASS and concrete negative FAIL_SIM_CORRECTNESS evidence.
