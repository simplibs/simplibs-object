from .validate_method_is_callable import validate_method_is_callable
from .validate_method_is_classmethod import validate_method_is_classmethod
from .validate_method_is_defined import validate_method_is_defined


_DESIGN_NOTES = """
# Classmethod Base Validation Sub-Package

## Purpose
Houses fundamental object nature, existence, and signature layout validation rules before deeper runtime metadata verification.

## Internal Components Registry

| Component                       | Type     | Description                                                                          |
| :------------------------------ | :------- | :----------------------------------------------------------------------------------- |
| `validate_method_is_callable`   | Function | Assures that the captured signature target can be actively invoked as a routine.     |
| `validate_method_is_classmethod`| Function | Assures the target is bounded as a true classmethod type descriptor inside the class. |
| `validate_method_is_defined`    | Function | Checks for target object presence within the target operational namespace context.   |
"""