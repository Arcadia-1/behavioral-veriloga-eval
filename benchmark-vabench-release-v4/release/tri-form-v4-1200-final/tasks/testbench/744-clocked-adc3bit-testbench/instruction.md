# Clocked ADC3bit Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked ADC3bit` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_EACH_RISING_CROSSING_OF_VCLK`: On each rising crossing of `vclk` through `vth_clk`, sample `vin` and quantize the `0 V` to `1 V` range into eight uniform lower-inclusive bins. Values below `0 V` clip to code `0`; values at or above `1 V` clip to code `7`. Drive `vd2`, `vd1`, and `vd0` as the binary representation of the held sampled code using `vh` for logic one and `0 V` for logic zero.
- `P_VTH_CLK_0_45_V_RISING`: `vth_clk = 0.45 V`: rising-edge threshold for `vclk`.
- `P_VH_0_9_V_LOGIC_HIGH`: `vh = 0.9 V`: logic-high output level.
- `P_VTH_CLK_0_45_V_RISING_2`: - `vth_clk = 0.45 V`: rising-edge threshold for `vclk`. - `vh = 0.9 V`: logic-high output level.
- `P_THE_OUTPUT_LOW_LEVEL_IS_0`: The output low level is `0 V`; the public input conversion range is `0 V` to `1 V`.
- `P_USE_DETERMINISTIC_VOLTAGE_DOMAIN_VERILOG_A`: Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, file I/O, random behavior, current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

The required trace names are: `time`, `vclk`, `vd0`, `vd1`, `vd2`, `vin`.

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
