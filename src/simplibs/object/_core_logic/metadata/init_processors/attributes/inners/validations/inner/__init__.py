from .validate_inner_is_class import validate_inner_is_class
from .validate_inner_is_not_simple_class import validate_inner_is_not_simple_class
from .validate_inner_is_simple_subclass import validate_inner_is_simple_subclass


_DESIGN_NOTES = """
# Inner Element Validation Sub-Package

## Purpose
Houses specialized type guards and architectural constraints evaluated against individual classes declared within the components sequence.

## Internal Components Registry

| Component                             | Type     | Description                                                                          |
| :------------------------------------ | :------- | :----------------------------------------------------------------------------------- |
| `validate_inner_is_class`             | Function | Ensures the target element is an abstract class type, rejecting raw data or instances.|
| `validate_inner_is_not_simple_class`  | Function | Blocks using bare framework base classes (`SimpleConstant`/`SimpleObject`) directly. |
| `validate_inner_is_simple_subclass`   | Function | Enforces framework lineage by verifying inheritance from the core base family tree.   |
"""