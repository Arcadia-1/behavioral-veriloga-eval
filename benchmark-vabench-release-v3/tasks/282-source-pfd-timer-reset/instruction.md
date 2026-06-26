# Source PFD Timer Reset

Implement a phase-frequency detector with delayed reset. A rising A edge asserts active-low UB; a rising B edge asserts D; when both have occurred, both reset after 100 ps.

The module name and port list must match `pfd_timer_reset.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `zhangz/L2_PFD.va`.
