# Task: vbm1_one_shot_timer_bugfix

The provided voltage-domain one-shot timer has a reset-priority bug: a reset
asserted while the output pulse is active does not immediately clear the pulse.
Fix the design so reset has priority over the pending one-shot timeout.

The fixed module must be named `one_shot_timer` and use electrical ports
`trig`, `rst_n`, and `pulse`. While `rst_n` is low, `pulse` must remain low and
any pending timeout must be disarmed. When `rst_n` is high, each rising `trig`
crossing should start one pulse of the configured width. If reset falls during
that pulse, the pulse should clear promptly rather than waiting for the timer.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
