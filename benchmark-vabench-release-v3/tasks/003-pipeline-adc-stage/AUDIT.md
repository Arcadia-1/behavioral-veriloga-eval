# Audit: 003 Pipeline ADC Stage

Gate 1: `independent_l1_ready`. This is a standalone 1.5-bit pipeline ADC
MDAC stage. It is independent from simple ADC/DAC transfer rows because it
combines sub-ADC decision coding with gain-two residue generation and clamping.

Gate 2: `cadence_modeling_ready`. The public prompt defines the PHI1/PHI2
sample/update timing, public thresholds around `VDD/2`, three decision regions,
digital output code mapping, residue equation, clamp behavior, and voltage-only
constraints. Current PR validation: EVAS gold PASS, Spectre AX hidden gold
PASS, and EVAS/Spectre negatives rejected with no Spectre errors. Spectre
emitted only environment/setup warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck covers middle, upper, lower, rail-clamp, and near-threshold
cases beyond the visible smoke scenario.

Checker coverage: `v3_003_pipeline_adc_stage` samples after PHI2 update events,
checks the expected two-bit code, compares residue against the public gain-two
MDAC behavior, and rejects wrong thresholds, code mapping, feedback polarity,
residue gain, and settling behavior.
