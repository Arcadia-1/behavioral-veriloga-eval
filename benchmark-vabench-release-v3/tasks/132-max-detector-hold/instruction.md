Implement a voltage-domain max detector.

The module must be named `max_detector_hold` and use this port order:

`vin, vout`

Initialize the held maximum from the input. Whenever `vin` is above the held
maximum, update the held value. Continuously drive `vout` to the held maximum.
