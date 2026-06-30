# Mixed Logic Clocked Voltage Sampler

Implement one Verilog-AMS source file named `mixed_logic_clocked_voltage_sampler.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Combine logic always sampling with analog voltage output.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `mixed_logic_clocked_voltage_sampler.vams`.
