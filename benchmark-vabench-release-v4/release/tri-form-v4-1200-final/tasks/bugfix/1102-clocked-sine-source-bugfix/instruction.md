# Clocked Sine Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `vin_src.va`: `vin_src`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_COMMON_MODE`: While RST_N is below vth, both outputs hold near vdd divided by two.
- `P_RISING_EDGE_SAMPLE`: After reset release, VOUT_P updates only on rising CLK crossings through vth.
- `P_SAMPLED_SINE`: At each qualifying clock edge, VOUT_P samples vdd/2 plus ampl times sin(2*pi*freq*time), plus the optional seeded perturbation.
- `P_REFERENCE_SIDE_COMMON_MODE`: VOUT_N remains at vdd divided by two during reset and active sampling.
- `P_INTEREDGE_HOLD`: Both outputs hold their sampled values between CLK events rather than continuously recomputing the sine or perturbation.
- `P_SEEDED_REPEATABILITY`: For fixed SEED, sigma, controls, and timing, the sampled perturbation sequence and outputs are repeatable; sigma zero removes the perturbation.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `vin_src.va`.
Every supplied `.va` file is editable; do not add or omit files.
