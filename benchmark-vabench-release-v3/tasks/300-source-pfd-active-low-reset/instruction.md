# Source PFD Active Low Reset

Implement a PFD with active-low UPB and active-high DOWN. A rising REF asserts UPB low; a rising FB asserts DOWN high; both reset after both edges arrive.

The module name and port list must match `pfd_active_low_reset.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `taoy/v_PFD.va`.
