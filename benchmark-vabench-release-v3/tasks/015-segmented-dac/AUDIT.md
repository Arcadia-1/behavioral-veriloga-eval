# Audit: 015 Segmented DAC

Gate 1: `independent_l1_ready`. This is a mixed binary-plus-thermometer DAC
transfer model. It is independent from pure binary and pure thermometer DAC
rows because the output combines two binary LSB controls with three thermometer
segments.

Gate 2: `cadence_modeling_ready`. The public prompt states interface, bit
order, binary weights, thermometer segment contribution, reference endpoints,
transition smoothing, and voltage-only constraints. Current PR validation:
EVAS gold PASS, Spectre AX hidden gold PASS, and EVAS/Spectre negatives
rejected with no Spectre errors. Spectre emitted only environment/setup
warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck samples representative binary-only, thermometer-only, mixed,
monotonic, and full-scale cases.

Checker coverage: `v3_015_segmented_dac` enforces the public segmented transfer
function and rejects wrong gain, wrong binary weights, swapped bits, missing
thermometer segment contribution, and scaling errors.
