# AGC Receiver Leveling Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `agc_receiver_leveling_loop.va`: `agc_receiver_leveling_loop`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_STATE`: Active-high reset restores out to 0.45 V, clears rssi_mon and metric, and represents the initial gain 2.2 on gain_mon.
- `P_CLOCKED_GAIN_LOOP`: The AGC samples and updates its held output and gain state only on rising clk crossings after reset releases.
- `P_OUTPUT_ENVELOPE`: Out is the current-gain amplification of vin about 0.45 V, clamped to 0.02 V through 0.88 V, and rssi_mon reports the normalized absolute output envelope.
- `P_GAIN_DIRECTION_AND_BOUNDS`: Envelope above target_amp plus deadband lowers gain by 0.18, envelope below target_amp minus deadband raises gain by 0.10, and gain remains in 0.45 through 3.0.
- `P_DEADBAND_HOLD`: When the observed envelope lies within the target deadband, the bounded gain state holds across the update.
- `P_SETTLING_METRIC`: Metric decreases with absolute envelope error from target_amp according to the public scaling and remains clamped to 0 V through 0.9 V.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `agc_receiver_leveling_loop.va`.
Every supplied `.va` file is editable; do not add or omit files.
