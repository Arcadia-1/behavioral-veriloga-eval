# Bugfix Companion: vbr1_l1_clocked_sample_and_hold

- Fixed source: `benchmark-vabench-release-v1/tasks/vbr1_l1_clocked_sample_and_hold/forms/dut/gold/sample_hold.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/vbr1_l1_clocked_sample_and_hold/forms/dut/gold/tb_sample_hold_ref.scs`
- Bug: The buggy sample-and-hold ignores the input sample and always holds zero.
- EVAS/Spectre status: pending fresh dual rerun

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
