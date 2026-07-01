# Audit: 002 Capacitive SAR Feedback DAC

Gate 1: `independent_l1_ready`. This is a reusable SAR ADC capacitive
feedback DAC model with a distinct calibration-code contribution. It is not a
duplicate of the simple voltage DAC, segmented DAC, thermometer DAC, or
subradix/weighted-decoder rows because the behavior is clocked, differential,
common-mode centered, and includes redundant calibration offset handling.

Gate 2: `cadence_modeling_ready`. The public prompt states the module
interface, parameters, sampled 10-bit main code, calibration-code contribution,
common-mode behavior, and voltage-only modeling constraints. Current PR
validation: EVAS gold PASS, Spectre AX hidden gold PASS, and EVAS/Spectre
negatives rejected with no Spectre errors. Spectre emitted only
environment/setup warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck exercises bit weights, calibration states, polarity, and
common-mode behavior beyond the visible smoke scenario.

Checker coverage: `v3_002_capacitive_weighted_sar_feedback_dac` evaluates the
public differential transfer contract from saved input/output traces and rejects
wrong gain, polarity, calibration weighting, and endpoint behavior.
