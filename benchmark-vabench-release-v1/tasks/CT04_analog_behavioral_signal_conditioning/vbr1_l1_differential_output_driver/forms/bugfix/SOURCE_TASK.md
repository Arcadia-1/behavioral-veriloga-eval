# Bugfix Companion: vbr1_l1_differential_output_driver

- Fixed source: `benchmark-vabench-release-v1/tasks/CT04_analog_behavioral_signal_conditioning/vbr1_l1_differential_output_driver/forms/dut/gold/differential_voltage_output_ref.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/CT04_analog_behavioral_signal_conditioning/vbr1_l1_differential_output_driver/forms/dut/gold/tb_differential_voltage_output_ref.scs`
- Bug: The buggy differential output driver ignores the enable input and continues driving a nonzero differential output while disabled.
- EVAS/Spectre status: pass in release dual evidence

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
