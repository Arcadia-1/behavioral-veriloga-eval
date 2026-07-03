# Differential Amplifier Core Audit

- Gate 1 counting status: retain as a small L1 analog primitive, with low complexity noted. It covers a differential-input single-ended gain core with input-referred offset.
- Gate 2 modeling status: prompt now states the differential input, offset, fixed gain, and voltage-domain boundary.
- Checker status: stable sampled waveform checks cover true differential input, offset subtraction, and fixed gain.
- Cadence reference anchor: differential voltage-domain macromodeling.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
