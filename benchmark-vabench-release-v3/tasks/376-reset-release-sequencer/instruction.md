# Reset Release Sequencer

Implement one Verilog-A source file named `reset_release_sequencer.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral DUT source for a clocked
reset-release sequencer that qualifies supply and bias before analog block
startup. Implement only the `reset_release_sequencer` module.

## Public Verilog-A Interface

```verilog
module reset_release_sequencer(clk, rst, supply_ok, bias_ok, stage1, stage2, ready, progress);
```

All ports are electrical. `clk` is the sequencing clock, `rst` is active-high
reset, `supply_ok` and `bias_ok` are voltage-coded qualification inputs, and
`stage1`, `stage2`, `ready`, and `progress` are voltage-coded observables.

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter integer final_stage = 3`.
- `parameter real tr = 60p`.

## Required Behavior

Initialize the internal stage count and all observables to zero. On each rising
clock crossing, clear the stage count when `rst` is high, `supply_ok <= vth`, or
`bias_ok <= vth`. Otherwise increment the stage count by one until it reaches
`final_stage`.

After updating the stage count, drive `stage1 = vhi` when `stage_count >= 1`,
`stage2 = vhi` when `stage_count >= 2`, and `ready = vhi` when
`stage_count >= final_stage`; otherwise drive each of those observables to
`0 V`. Drive `progress = vhi * clip01(stage_count / final_stage)`. Hold the
last observable values between rising clock crossings.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Use local analog helper functions
rather than user `task`/`endtask` syntax. Do not use Verilog-AMS digital
kernels, branch current contributions, transistor devices, `ddt()`, or
`idt()`. Do not hard-code testbench stimulus times.

## Output Contract

Return only `reset_release_sequencer.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
