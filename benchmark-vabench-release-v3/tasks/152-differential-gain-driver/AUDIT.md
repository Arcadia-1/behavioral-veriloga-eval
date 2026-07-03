# Differential Gain Driver Audit

- Gate 1 counting status: retain as an L1 differential driver. The function is balanced output-pair generation around a reference node, not only scalar gain.
- Gate 2 modeling status: prompt now exposes the `gain` parameter and the half-swing split around `sigref`.
- Checker status: stable sampled waveform checks cover output symmetry, gain split, and polarity.
- Cadence reference anchor: differential voltage-domain macromodeling and explicit reference/common-mode handling.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
