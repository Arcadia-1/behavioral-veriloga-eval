# Source Single Shot Timer Pulse

Implement a single-shot pulse generator. A rising VIN crossing asserts VOUT high after delay and a timer deasserts it after the configured pulse width.

The module name and port list must match `single_shot_timer_pulse.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/single_shot.va`.
