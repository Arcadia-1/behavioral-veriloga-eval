# Source Offset Halving Search

Implement an offset-search voltage driver. On each CLK falling edge, read DCMPP as the comparator decision, update the signed search residue, halve the step size, and drive VINP/VINN symmetrically around mid-supply.

The module name and port list must match `offset_halving_search.va`. Keep the model voltage-domain only and deterministic. The historical source normalized for this task is `zhangym/_va_offset.va`.
