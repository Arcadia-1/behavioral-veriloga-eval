# Honest SOP Audit: Task 001 Bang-Bang Phase Detector

## Scope

Task boundary is one Verilog-A DUT, `bbpd_ref.va`, plus EVAS/Spectre-compatible `.scs` testbenches.

## Four Standards

- Useful scenario: BBPD direction logic is a common CDR/PLL behavioral model primitive.
- Reasonable task: the public prompt states the exact data-edge decision table, output pulse behavior, and port order.
- Complete tests: hidden `.scs` covers rising/falling data edges, both correction directions, no-correction cases, and pulse clearing on the next clock transition.
- Fair evaluation: checker derives expected UP/DOWN behavior from the public decision table and concrete negatives compile but should fail behavior.

Certification status: certified. EVAS gold PASS; 5/5 concrete negatives compile and fail with FAIL_SIM_CORRECTNESS.
