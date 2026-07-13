# Flash Folded DAC4 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `flash_folded_dac4.va`: `flash_folded_dac4`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TREAT_EACH_INPUT_BIT_AS_LOGIC`: Treat each input bit as logic one when its voltage is above `vth`. The MSB selects the folded half of the transfer. When `vd4` is high, add the lower-bit weighted value above midscale. When `vd4` is low, subtract the lower-bit weighted value from midscale. The lower bits use binary weights `4`, `2`, and `1`, and the output is scaled by `vref/16`.
- `P_VTH_0_45_V_DECISION_THRESHOLD`: `vth = 0.45 V`: decision threshold for each voltage-coded input bit.
- `P_VREF_1_0_V_OUTPUT_REFERENCE`: `vref = 1.0 V`: output reference/full-scale voltage.
- `P_VTH_0_45_V_DECISION_THRESHOLD_2`: - `vth = 0.45 V`: decision threshold for each voltage-coded input bit. - `vref = 1.0 V`: output reference/full-scale voltage.
- `P_USE_DETERMINISTIC_VOLTAGE_DOMAIN_VERILOG_A`: Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `flash_folded_dac4.va`.
Every supplied `.va` file is editable; do not add or omit files.
