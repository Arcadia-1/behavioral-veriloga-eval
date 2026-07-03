# Variable Gain Differential Amplifier Audit

- Gate 1 counting status: duplicate-risk L1 candidate. It is a valid voltage-controlled differential gain block, but functionally overlaps strongly with `160-voltage-controlled-gain-amplifier` and `280-vargain-diffamp-clip`.
- Recommended counting treatment: retain only if the benchmark set wants a fixed-midpoint, no-input-offset variant; otherwise prefer `280` as the more parameterized canonical variable-gain differential clip task.
- Gate 2 modeling status: prompt now exposes the differential input/control product, fixed midpoint, gain constant, clamp window, and voltage-domain boundary.
- Checker status: stable sampled waveform checks cover differential control, midpoint, and clamp behavior.
- Cadence reference anchor: voltage-domain gain/control macromodels with explicit limiting.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
