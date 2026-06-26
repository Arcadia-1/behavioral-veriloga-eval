# Source Deadband Diffamp

Implement a differential deadband amplifier. Inside +/-100 mV it outputs 20 mV leakage; outside it applies asymmetric low/high gains.

The module name and port list must match `deadband_diffamp.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/deadband_diffamp.va`.
