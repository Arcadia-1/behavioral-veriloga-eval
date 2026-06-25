# Source PFD Up Down State

Implement a bounded phase-frequency detector state machine. REF rising increments state up to +1, FB rising decrements state down to -1, and U/D expose the sign of the state.

The module name and port list must match `pfd_up_down_state.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `huangsy/PFD.va`.
