# Source DFF Set Reset

Implement a voltage-coded D flip-flop with active-low asynchronous SETB/RSTB and complementary outputs. Clock rising samples D when both async controls are inactive.

The module name and port list must match `dff_set_reset.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `gaoya/L4_DFF_VA.va`.
