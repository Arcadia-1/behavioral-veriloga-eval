# Clocked ADC3bit

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clocked_adc3bit.va`: `clocked_adc3bit`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_EACH_RISING_CROSSING_OF_VCLK`: On each rising crossing of `vclk` through `vth_clk`, sample `vin` and quantize the `0 V` to `1 V` range into eight uniform lower-inclusive bins. Values below `0 V` clip to code `0`; values at or above `1 V` clip to code `7`. Drive `vd2`, `vd1`, and `vd0` as the binary representation of the held sampled code using `vh` for logic one and `0 V` for logic zero.
- `P_VTH_CLK_0_45_V_RISING`: `vth_clk = 0.45 V`: rising-edge threshold for `vclk`.
- `P_VH_0_9_V_LOGIC_HIGH`: `vh = 0.9 V`: logic-high output level.
- `P_VTH_CLK_0_45_V_RISING_2`: - `vth_clk = 0.45 V`: rising-edge threshold for `vclk`. - `vh = 0.9 V`: logic-high output level.
- `P_THE_OUTPUT_LOW_LEVEL_IS_0`: The output low level is `0 V`; the public input conversion range is `0 V` to `1 V`.
- `P_USE_DETERMINISTIC_VOLTAGE_DOMAIN_VERILOG_A`: Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, file I/O, random behavior, current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clocked_adc3bit.va`.
Do not add or omit artifacts.
