from .EqualizerProtocol import EqualizerProtocol
from .VolumeProtocol import VolumeProtocol

_DESIGN_NOTES = """
# Numerical Mixin Protocols Sub-Package

## Purpose
Provides high-level protocols for numerical manipulation mixins, binding single-value steppers
or multi-node equalizer controllers to object instances.

## Internal Components Registry

| Component           | Type     | Description                                                                  |
| :------------------ | :------- | :--------------------------------------------------------------------------- |
| `EqualizerProtocol` | Protocol | Interface for node compositions exposing dynamic stepper properties.         |
| `VolumeProtocol`    | Protocol | Interface for instances with a bound primary value stepper controller.       |
"""