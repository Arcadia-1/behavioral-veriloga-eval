# Vargain Diffamp Clip

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `vargain_diffamp_clip.va`: `vargain_diffamp_clip`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_COMPUTE_THE_DIFFERENTIAL_SIGNAL_AS_V`: Compute the observable input signal as `V(sigin_p, sigin_n)`.
- `P_COMPUTE_THE_DIFFERENTIAL_CONTROL_AS_V`: Compute the gain-control term as `V(sigctrl_p, sigctrl_n)` with the documented polarity.
- `P_SUBTRACT_SIGIN_OFFSET_FROM_THE_DIFFERENTIAL`: Subtract `sigin_offset` from the differential input before gain multiplication.
- `P_MULTIPLY_THE_OFFSET_CORRECTED_SIGNAL_BY`: Multiply the offset-corrected signal by the differential control and `gain_const`.
- `P_CLAMP_THE_RESULT_TO_THE_PUBLIC`: Clamp the amplified target to the public positive and negative output limits.
- `P_DRIVE_SIGOUT_WITH_THE_CLIPPED_TARGET`: Drive `sigout` with the clipped target transfer and correct output scale.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `vargain_diffamp_clip.va`.
Do not add or omit artifacts.
