# Bugfix Companion: vbr1_l1_clocked_comparator

- Fixed source: `benchmark-vabench-release-v1/tasks/vbr1_l1_clocked_comparator/forms/dut/gold/cmp_strongarm.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/vbr1_l1_clocked_comparator/forms/dut/gold/tb_cmp_strongarm_ref.scs`
- Bug: The buggy clocked comparator never asserts the negative-side decision output.
- EVAS/Spectre status: pending fresh dual rerun

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
