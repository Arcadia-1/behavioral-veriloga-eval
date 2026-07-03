# Limiter Rails Audit

- Gate 1 counting status: retain as an L1 analog primitive. The task covers a supply-referenced voltage limiter with explicit headroom inputs.
- Gate 2 modeling status: prompt now exposes the supply-referenced upper/lower limits and asks for one continuous voltage contribution after computing the clipped target.
- Checker status: stable sampled waveform checks cover pass-through, upper clamp, and lower clamp behavior.
- Cadence reference anchor: limiting/region models should compute a target region and then contribute a voltage, avoiding branch-switched potential contributions when possible.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold. The previous branch-switched contribution lint warning was removed by computing a target before the voltage contribution.
