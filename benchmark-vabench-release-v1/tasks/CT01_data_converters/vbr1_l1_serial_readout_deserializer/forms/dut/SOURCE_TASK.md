# Source Task

This release task is a designed duplicate-pruning replacement for `vbr1_l1_event_pulse_stretcher` after duplicate-pruning and control/readout category removal.

- Release entry: `vbr1_l1_serial_readout_deserializer`
- Form: `dut`
- Function: Serial readout deserializer
- Rationale: Serial ADC/readout word capture is a mixed-signal readout/control interface function not already covered by CT01-CT05 primitives.
- Certification status: static guardrail only until fresh EVAS/Spectre dual validation.
