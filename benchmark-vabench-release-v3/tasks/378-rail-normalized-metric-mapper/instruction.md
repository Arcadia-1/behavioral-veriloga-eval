# Rail Normalized Metric Mapper

## Task Contract

Build a Spectre-compatible voltage-domain behavioral model for Rail-aware metric normalizer for voltage-domain measurement support across shifted local supplies.

This is a DUT source task. Implement only the `rail_normalized_metric_mapper` module; no external validation code, transistor devices, or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module rail_normalized_metric_mapper(meas, vdd, vss, en, norm, valid);
```

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter real span_min = 0.60`.
- `parameter real span_max = 1.20`.
- `parameter real tr = 50p`.

## Required Behavior

- Normalize meas relative to the local V(vdd,vss) span and vss rail.
- Clip the normalized metric to the public voltage-coded range.
- Assert valid only when enable is high, supply span is valid, and the measurement lies inside the local rail window.
- Clear norm and valid while disabled or under the minimum supply span.
- Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code testbench-specific stimulus timing.

## Output Contract

Return only `rail_normalized_metric_mapper.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
