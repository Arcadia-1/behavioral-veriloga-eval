# Configurable Startup Policy

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `configurable_startup_policy.va`: `configurable_startup_policy`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Clear all observables when `en` is low or when the local supply span is outside the public range. Drive `out` with the task-specific bounded analog result, drive `flag` with the task-specific qualification condition, and drive `metric` with a bounded diagnostic magnitude.
- `P_BUILD_A_VOLTAGE_DOMAIN_ANALOG_MIXED`: Build a voltage-domain analog/mixed-signal helper or monitor. Parameter-style startup policy selector replacing unsupported preprocessor variants with runtime-observable behavior.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for voltage-coded controls.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for output observables.
- `P_SPAN_MIN_0_62_V_SPAN`: `span_min = 0.62 V`, `span_max = 1.28 V`: legal local supply span measured as
- `P_TR_50P_OUTPUT_TRANSITION_SMOOTHING_TIME`: `tr = 50p`: output transition smoothing time.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `configurable_startup_policy.va`.
Do not add or omit artifacts.
