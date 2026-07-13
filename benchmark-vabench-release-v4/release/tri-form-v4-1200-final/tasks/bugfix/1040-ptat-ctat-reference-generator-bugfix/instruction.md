# PTAT CTAT Reference Generator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ptat_ctat_reference_generator.va`: `ptat_ctat_reference_generator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_REFERENCE`: Reset initializes out to 0.45 V and metric to 0 V until a valid rising-clock update.
- `P_INPUT_CLAMP`: Each rising clk update with reset inactive samples vin and clamps the temperature/control value to 0 V through 0.9 V.
- `P_PTAT_TREND`: Metric reports the PTAT branch 0.18 V plus 0.34 times the clamped sampled input and therefore increases monotonically with vin.
- `P_CTAT_PTAT_AVERAGE`: Out is the equal-weight average of PTAT = 0.18 V + 0.34*vin_clamped and CTAT = 0.78 V - 0.34*vin_clamped.
- `P_REFERENCE_BOUNDS`: Out remains within the public 0 V through 0.9 V voltage range with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ptat_ctat_reference_generator.va`.
Every supplied `.va` file is editable; do not add or omit files.
