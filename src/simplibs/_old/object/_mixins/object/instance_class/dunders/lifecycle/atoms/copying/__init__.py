from .Copy import CopyMixin
from .Deepcopy import DeepcopyMixin

__all__ = (
    "CopyMixin",
    "DeepcopyMixin",
)


__DOCT__ = """
## `lifecycle/copying/`

> **Subgroup purpose:**
> Controls how objects are duplicated and serialized. Python distinguishes shallow copy
> (a new container pointing to the same objects), deep copy (a fully independent clone),
> and pickle serialization (converting the object to bytes and back). All of these have
> dedicated hooks so you can customise the behaviour for your class.
"""