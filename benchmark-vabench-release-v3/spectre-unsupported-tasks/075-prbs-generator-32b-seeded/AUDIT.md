# SOP Audit: PRBS Generator 32b Seeded

- Useful scenario: testbench utility module for behavioral Verilog-A validation flows.
- Reasonable task: public prompt states the scored interface and deterministic behavior.
- Complete tests: visible smoke plus EVAS/Spectre-compatible transient validation.
- Fair evaluation: private checker logic derives expected behavior from the public contract and concrete negative variants are expected to compile but fail correctness.

Certification status: certified with EVAS gold PASS and concrete negative FAIL_SIM_CORRECTNESS evidence.
