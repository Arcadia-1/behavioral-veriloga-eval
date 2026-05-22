# Bugfix Companion: vbr1_l1_xor_phase_detector

- Fixed source: `benchmark-vabench-release-v1/tasks/vbr1_l1_xor_phase_detector/forms/dut/gold/xor_phase_detector_ref.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/vbr1_l1_xor_phase_detector/forms/dut/gold/tb_xor_phase_detector_ref.scs`
- Bug: The buggy phase detector implements XNOR instead of XOR.
- EVAS/Spectre status: pending fresh dual rerun

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
