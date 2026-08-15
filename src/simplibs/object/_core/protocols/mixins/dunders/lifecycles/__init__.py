from .CopyableProtocol import CopyableProtocol
from .LifecycleProtocol import LifecycleProtocol
from .PickleReduceProtocol import PickleReduceProtocol
from .PickleStateProtocol import PickleStateProtocol

_DESIGN_NOTES = """
# Lifecycles Dunder Protocols Sub-Package

## Purpose
Provides protocols governing object replication, state freezing, restoration, and serialization hooks.

## Internal Components Registry

| Component              | Type     | Description                                                                  |
| :--------------------- | :------- | :--------------------------------------------------------------------------- |
| `CopyableProtocol`     | Protocol | Interface for shallow (`__copy__`) and deep (`__deepcopy__`) copying.        |
| `LifecycleProtocol`    | Protocol | Master structural aggregator combining copying and pickle protocols.         |
| `PickleReduceProtocol` | Protocol | Low-level pickle protocol interface via factory reconstruction (`__reduce__`).|
| `PickleStateProtocol`  | Protocol | State persistence interface using `__getstate__` and `__setstate__`.         |
"""