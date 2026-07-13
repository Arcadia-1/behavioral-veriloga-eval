# Edge Delay Line with Deglitch Window

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `edge_delay_line_deglitch.va`: `edge_delay_line_deglitch`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: When rst is above vth or enable is at or below vth, pending edge state is cancelled and vout, edge_valid, and rejected settle to vss no later than the next scheduling tick.
- `P_STABLE_EDGE_QUALIFICATION`: A rising or falling vin crossing through vth can qualify only when vin remains in the crossed-to logic state for min_width_ticks scheduling ticks while reset is inactive and the DUT is enabled.
- `P_DELAYED_EDGE_EMISSION`: After an input edge qualifies, vout changes to the corresponding vdd or vss target only after the additional delay_ticks scheduling interval and does not change early.
- `P_NARROW_GLITCH_REJECTION`: If vin reverses before a pending edge completes qualification, that edge does not update vout and rejected produces a bounded high pulse.
- `P_VALID_EMISSION_PULSE`: Each qualified delayed update of vout produces one bounded high pulse on edge_valid, while rejected remains reserved for cancelled narrow edges.
- `P_BIDIRECTIONAL_LEVELS`: Qualified rising and falling input edges can respectively drive vout toward vdd and vss, and all public outputs use tr-smoothed voltage transitions.
- `P_PARAMETER_OVERRIDE`: Overriding tick, min_width_ticks, or delay_ticks changes the observable qualification or emission timing without changing module ports, output polarity, or reset/enable behavior.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `edge_delay_line_deglitch.va`.
Do not add or omit artifacts.
