# Attenuator Gain Audit

- Gate 1 counting status: retain as an L1 analog primitive. The task covers dB-to-linear voltage attenuation, which is a distinct gain-block contract rather than only a renamed linear amplifier.
- Gate 2 modeling status: prompt now exposes the module, `attenuation` parameter, voltage-domain boundary, and dB amplitude-ratio behavior without referencing private evaluator details.
- Checker status: stable sampled waveform checks cover input scaling at the configured attenuation.
- Cadence reference anchor: basic voltage-domain macromodel guidance; no transistor-level or current-domain behavior is expected.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
