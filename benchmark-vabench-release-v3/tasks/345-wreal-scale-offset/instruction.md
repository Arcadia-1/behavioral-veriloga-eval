# Wreal Scale Offset

Implement one Verilog-AMS source file named `wreal_scale_offset.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Use wreal affine scaling with continuous assign.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `wreal_scale_offset.vams`.
