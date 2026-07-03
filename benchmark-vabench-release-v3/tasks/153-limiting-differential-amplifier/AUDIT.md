# Limiting Differential Amplifier Audit

- Gate 1 counting status: retain as an L1 limiting differential amplifier. It combines differential gain, input offset, rail midpoint centering, and output limiting.
- Gate 2 modeling status: prompt now exposes all public parameters and the target-then-clamp modeling contract.
- Checker status: stable sampled waveform checks cover input offset, rail midpoint, and output clipping.
- Cadence reference anchor: region/limiting macromodels should make boundary behavior explicit and keep contributions voltage-domain.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
