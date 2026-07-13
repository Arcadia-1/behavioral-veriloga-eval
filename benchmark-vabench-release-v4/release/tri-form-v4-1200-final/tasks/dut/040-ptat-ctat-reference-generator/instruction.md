# PTAT CTAT Reference Generator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ptat_ctat_reference_generator.va`: `ptat_ctat_reference_generator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_REFERENCE`: Reset initializes out to 0.45 V and metric to 0 V until a valid rising-clock update.
- `P_INPUT_CLAMP`: Each rising clk update with reset inactive samples vin and clamps the temperature/control value to 0 V through 0.9 V.
- `P_PTAT_TREND`: Metric reports the PTAT branch 0.18 V plus 0.34 times the clamped sampled input and therefore increases monotonically with vin.
- `P_CTAT_PTAT_AVERAGE`: Out is the equal-weight average of PTAT = 0.18 V + 0.34*vin_clamped and CTAT = 0.78 V - 0.34*vin_clamped.
- `P_REFERENCE_BOUNDS`: Out remains within the public 0 V through 0.9 V voltage range with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ptat_ctat_reference_generator.va`.
Do not add or omit artifacts.
