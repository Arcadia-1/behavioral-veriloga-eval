# Power Enable Turn-On Delay Gate Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Power Enable Turn-On Delay Gate` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_ON_EACH_RISING_CROSSING_OF_CLK`: On each rising crossing of `clk`, evaluate whether supply, bias, enable, and power-down conditions allow operation. Drive `pwr_ok` high whenever the sampled conditions are valid, meaning `vdd_min <= V(vdd, vss) <= vdd_max`, `vbias_min <= V(vbias, vss) <= vbias_max`, `V(en) > vth`, and `V(pd) <= vth`. Maintain an integer consecutive-valid counter. Increment the counter by one on each sampled valid rising-clock update until it reaches `delay_cycles`; reset the counter to zero on any sampled invalid update. After applying that update, assert `drive_en` when the counter is greater than or equal to `delay_cycles`. Drive `delay_mon = min(vhi, vhi * counter / delay_cycles)` as the bounded voltage-coded turn-on progress value from `0 V` to `vhi`. Smooth all outputs with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_POWER_SEQUENCING`: Build a voltage-domain power sequencing DUT for a biased analog block. The module samples supply, bias, enable, and power-down conditions, reports sampled power validity, and releases downstream drive only after a consecutive valid turn-on delay.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `clk`, `en`, and `pd`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for voltage-coded outputs.
- `P_VDD_MIN_0_75_V_VDD`: `vdd_min = 0.75 V`, `vdd_max = 1.05 V`: valid `V(vdd, vss)` window.
- `P_VBIAS_MIN_0_25_V_VBIAS`: `vbias_min = 0.25 V`, `vbias_max = 0.75 V`: valid `V(vbias, vss)` window.

The required trace names are: `time`, `clk`, `delay_mon`, `drive_en`, `en`, `pd`, `pwr_ok`, `vbias`, `vdd`, `vss`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
