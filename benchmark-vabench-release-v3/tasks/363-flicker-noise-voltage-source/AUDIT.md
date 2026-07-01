# Honest SOP Audit: Flicker Noise Voltage Source

## Scope

This task belongs to the noise/analysis extension set. It is not part of the original full-300 Verilog-A transient certification claim.

## Four Standards

- Useful scenario: exercises `Use flicker_noise() as a behavioral 1/f noise contribution.`
- Reasonable task: the public prompt fixes the target artifact and keeps the model behavioral.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile under an AC/noise-capable simulator while changing small behavior details that should fail full checks.

Certification status: noise-analysis-candidate. EVAS currently parses these functions but does not compile them; track EVAS issue #23: https://github.com/Arcadia-1/EVAS/issues/23 before EVAS certification.
