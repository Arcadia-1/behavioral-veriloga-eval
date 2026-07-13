# Rail Ramp Rate Startup Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `rail_ramp_rate_startup_monitor.va`: `rail_ramp_rate_startup_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RAIL_OK_ENFORCES_ENABLE_AND_SUPPLY_WINDOW`: Drive rail_ok high only while enabled and the sampled local supply lies inside the public operating window.
- `P_RAMP_OK_QUALIFIES_STARTUP_AND_SETTLING_SLEW`: Before vready, accept only positive sampled movement within dv_min..dv_max; at or above vready, accept only absolute movement no larger than dv_settle_max.
- `P_STARTUP_READY_REQUIRES_CONSECUTIVE_SETTLED_SAMPLES`: Assert startup_ready only after ready_cycles consecutive samples satisfy rail, ramp, and vready qualification; clear the count on any invalid sample.
- `P_SLEW_METRIC_REPORTS_BOUNDED_DELTA`: Drive slew_metric as vhi times the sampled absolute rail delta divided by dv_max, clipped to zero through one.
- `P_ON_EACH_RISING_CROSSING_OF_CLK`: On each rising crossing of `clk`, sample `V(vdd, vss)` and compute the sampled change from the previous clock update. Drive `rail_ok` high only while `en` is high and the sampled local supply is inside the public operating window. Before the sampled rail reaches `vready`, drive `ramp_ok` high only when the sampled positive rail movement is between `dv_min` and `dv_max`. Once the sampled rail is at or above `vready`, drive `ramp_ok` high only when the absolute sampled movement is no larger than `dv_settle_max`. Accumulate consecutive settled samples only when `rail_ok` is high, `ramp_ok` is high, and the rail is at or above `vready`; clear that accumulator on any sampled invalid condition. Assert `startup_ready` only after `ready_cycles` consecutive settled updates. Drive `slew_metric` as `vhi * clip(abs(delta_v) / dv_max, 0, 1)`. Smooth the voltage-coded outputs with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_STARTUP_MONITOR`: Build a voltage-domain startup monitor for a locally supplied analog block. The module samples the local rail on a clock, checks whether the rail is inside the allowed operating window, qualifies the startup ramp rate, and releases a startup-ready flag only after the rail has settled for consecutive sampled updates.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `clk` and `en`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for voltage-coded outputs.
- `P_VDD_MIN_0_72_V_VDD`: `vdd_min = 0.72 V`, `vdd_max = 1.08 V`: valid `V(vdd, vss)` operating
- `P_VREADY_0_86_V_SAMPLED_RAIL`: `vready = 0.86 V`: sampled rail level above which settling qualification is

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `rail_ramp_rate_startup_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
