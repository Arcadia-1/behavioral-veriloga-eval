# Bugfix Companion: vbr1_l1_window_comparator_detector

- Fixed source: `benchmark-vabench-release-v1/tasks/vbr1_l1_window_comparator_detector/forms/dut/gold/cross_hysteresis_window_ref.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/vbr1_l1_window_comparator_detector/forms/dut/gold/tb_cross_hysteresis_window_ref.scs`
- Bug: The buggy window comparator collapses the falling threshold onto the rising threshold.
- EVAS/Spectre status: pending fresh dual rerun

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
