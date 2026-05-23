# Source Task

This release task is a designed duplicate-pruning replacement for `vbr1_l1_edge_detector` after duplicate-pruning and control/readout category removal.

- Release entry: `vbr1_l1_adc_code_capture_register`
- Form: `bugfix`
- Function: ADC code capture register
- Rationale: ADC/readout code capture and overrange latch is a mixed-signal readout/control interface function not already covered by CT01-CT05 primitives.
- Certification status: static guardrail only until fresh EVAS/Spectre dual validation.
