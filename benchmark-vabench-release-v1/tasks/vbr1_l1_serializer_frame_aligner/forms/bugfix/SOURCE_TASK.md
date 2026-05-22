# Bugfix Companion: vbr1_l1_serializer_frame_aligner

- Fixed source: `benchmark-vabench-release-v1/tasks/vbr1_l1_serializer_frame_aligner/forms/dut/gold/serializer_frame_alignment_ref.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/vbr1_l1_serializer_frame_aligner/forms/dut/gold/tb_serializer_frame_alignment_ref.scs`
- Bug: The buggy serializer emits the loaded word in the reverse bit order.
- EVAS/Spectre status: pending fresh dual rerun

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
