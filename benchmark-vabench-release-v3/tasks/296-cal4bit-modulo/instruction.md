# CAL4bit Floor-Clamped Encoder

Implement a scalar-to-4-bit calibration encoder. The input voltage is rounded down to an integer code, clamped to the valid 4-bit range, and emitted as four voltage-coded bits.

The module name and port list must match `cal4bit_modulo.va`. Keep the implementation deterministic and voltage-domain only. Despite the historical module name, the public behavior is floor-then-clamp encoding, not modulo wrapping.
