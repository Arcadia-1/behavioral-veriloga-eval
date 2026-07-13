# Edge Delay Qualified Driver Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `edge_delay_qualified_driver.va`: `edge_delay_qualified_driver`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Clear all observables when `en` is low or when the local supply span is outside the public range. The DUT updates its observable state on the public clock edge and clears state while reset is high. Drive `out` with the task-specific bounded analog result, drive `flag` with the task-specific qualification condition, and drive `metric` with a bounded diagnostic magnitude.
- `P_BUILD_A_VOLTAGE_DOMAIN_ANALOG_MIXED`: Build a voltage-domain analog/mixed-signal helper or monitor. Clock-edge qualified delay-style driver replacing specify/specparam timing with explicit event state.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for voltage-coded controls.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for output observables.
- `P_SPAN_MIN_0_62_V_SPAN`: `span_min = 0.62 V`, `span_max = 1.28 V`: legal local supply span measured as
- `P_TR_50P_OUTPUT_TRANSITION_SMOOTHING_TIME`: `tr = 50p`: output transition smoothing time.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `edge_delay_qualified_driver.va`.
Every supplied `.va` file is editable; do not add or omit files.
