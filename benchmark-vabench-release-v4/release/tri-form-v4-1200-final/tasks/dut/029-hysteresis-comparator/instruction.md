# Hysteresis Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cmp_hysteresis.va`: `cmp_hysteresis`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_DECISION`: OUTP initializes high only when the initial differential exceeds positive vhys over two; otherwise OUTP initializes low and OUTN high.
- `P_POSITIVE_SWITCH_THRESHOLD`: The low OUTP state switches high only on a rising differential crossing of positive vhys over two.
- `P_NEGATIVE_SWITCH_THRESHOLD`: The high OUTP state switches low only on a falling differential crossing of negative vhys over two.
- `P_HYSTERESIS_HOLD`: The previous decision is retained while the differential remains inside the hysteresis band.
- `P_COMPLEMENTARY_RAIL_OUTPUT`: OUTP and OUTN remain complementary and use the local VDD and VSS rail levels after smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cmp_hysteresis.va`.
Do not add or omit artifacts.
