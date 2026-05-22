# Bugfix Companion: vbr1_l1_pfd_small_phase_error_response

- Fixed source: `benchmark-vabench-release-v1/tasks/CT05_pll_clock_event_timing/vbr1_l1_pfd_small_phase_error_response/forms/dut/gold/pfd_updn.va`
- Reference testbench: `benchmark-vabench-release-v1/tasks/CT05_pll_clock_event_timing/vbr1_l1_pfd_small_phase_error_response/forms/dut/gold/tb_pfd_small_phase_ref.scs`
- Bug: The buggy PFD omits the mutual reset path when both REF and DIV edges have arrived.
- EVAS/Spectre status: pass in release dual evidence

This bugfix form was created only where a single-cause badcase
could be reconstructed from existing release gold. It is not
imported as historical certification evidence.
