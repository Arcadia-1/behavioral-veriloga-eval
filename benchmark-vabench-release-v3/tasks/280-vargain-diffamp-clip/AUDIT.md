# Vargain Diffamp Clip Audit

- Gate 1 counting status: retain as the strongest L1 representative of the variable-gain differential clip family. It is parameterized by gain constant, input offset, and output limits.
- Duplicate relationship: overlaps with `159-variable-gain-differential-amplifier` and `160-voltage-controlled-gain-amplifier`; this task is the preferred canonical retained version if the set is de-duplicated strictly.
- Gate 2 modeling status: prompt now exposes all public parameters, differential input/control roles, target computation, clipping limits, and voltage-domain boundary.
- Checker status: stable sampled waveform checks cover offset, control polarity, gain scaling, positive clip, and negative clip behavior through gold and negative variants.
- Cadence reference anchor: voltage-domain gain/control macromodels with explicit limiting and real target variables before contribution.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
