# Latched Bus DAC8 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `latched_bus_dac8.va`: `latched_bus_dac8`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_CAPTURE`: Each rising crossing of vclk through vth captures the unsigned value of b[7:0].
- `P_HOLD_BETWEEN_EDGES`: vout retains the value from the most recent rising clock crossing despite input-bus changes between update edges.
- `P_ENDPOINTS`: Latched code 0 maps to 0 V and latched code 255 maps to vref.
- `P_BINARY_MONOTONICITY`: Increasing the latched unsigned code never decreases vout, with b7 as MSB and b0 as LSB.
- `P_OUTPUT_SMOOTHING`: vout approaches each newly latched target with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `latched_bus_dac8.va`.
Every supplied `.va` file is editable; do not add or omit files.
