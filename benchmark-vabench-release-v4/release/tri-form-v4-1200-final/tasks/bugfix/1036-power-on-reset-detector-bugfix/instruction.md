# Power-On Reset Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `power_on_reset_detector.va`: `power_on_reset_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_ASSERTED_UNSAFE`: Out is active-high reset and remains asserted while rst is high or vin is below vtrip.
- `P_DELAYED_RELEASE`: After rst releases and vin is power-good, out stays asserted for four rising clk updates before deasserting.
- `P_RELEASE_STATUS`: Metric uses an intermediate status level during the release delay, is high after delayed reset release completes, and is cleared when reset is reasserted or supply is not power-good.
- `P_FAULT_REASSERTION`: A new reset assertion or a brownout below vtrip immediately reasserts out and clears the accumulated release delay, independent of the next clk edge.
- `P_VOLTAGE_CODED_LEVELS`: Out and metric use bounded voltage-coded low and high levels with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `power_on_reset_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
