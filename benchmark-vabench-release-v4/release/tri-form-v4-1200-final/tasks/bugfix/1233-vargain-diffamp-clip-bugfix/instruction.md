# Vargain Diffamp Clip Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `vargain_diffamp_clip.va`: `vargain_diffamp_clip`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_COMPUTE_THE_DIFFERENTIAL_SIGNAL_AS_V`: Compute the observable input signal as `V(sigin_p, sigin_n)`.
- `P_COMPUTE_THE_DIFFERENTIAL_CONTROL_AS_V`: Compute the gain-control term as `V(sigctrl_p, sigctrl_n)` with the documented polarity.
- `P_SUBTRACT_SIGIN_OFFSET_FROM_THE_DIFFERENTIAL`: Subtract `sigin_offset` from the differential input before gain multiplication.
- `P_MULTIPLY_THE_OFFSET_CORRECTED_SIGNAL_BY`: Multiply the offset-corrected signal by the differential control and `gain_const`.
- `P_CLAMP_THE_RESULT_TO_THE_PUBLIC`: Clamp the amplified target to the public positive and negative output limits.
- `P_DRIVE_SIGOUT_WITH_THE_CLIPPED_TARGET`: Drive `sigout` with the clipped target transfer and correct output scale.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `vargain_diffamp_clip.va`.
Every supplied `.va` file is editable; do not add or omit files.
