# LC VCO Behavioral Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lc_vco_behavioral_source.va`: `lc_vco_behavioral_source`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CENTER`: Reset or disable centers both oscillator outputs at vcm and clears metrics and valid.
- `P_CONTROL_FREQUENCY_MAP`: Enabled edge periods follow the linear clamped vctrl mapping from fmin to fmax without retiming an already pending edge.
- `P_COMPLEMENTARY_AMPLITUDE`: Enabled oscillator outputs are complementary around vcm with the declared amplitude.
- `P_METRIC_REPORTING`: freq_metric reports clamped vctrl and amp_metric reports amplitude while enabled.
- `P_VALID_AFTER_TWO_CYCLES`: valid remains low until two complete oscillator cycles have elapsed after enable.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lc_vco_behavioral_source.va`.
Every supplied `.va` file is editable; do not add or omit files.
