from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def _exception_info_for_default(
    owner_class: "SimpleClassLike",
):
    """Extracts shared metadata and structural context for default value exception generation."""
    attribute_name = "_default"
    class_name = owner_class.__name__
    class_parent = "SimpleObject" if "SimpleObject" in owner_class.__mro__ else "SimpleConstant"
    error_name = "INVALID DEFAULT DEFINITION"
    context = f"Metadata evaluation and validation for: {class_name}.{attribute_name}"

    return class_name, class_parent, error_name, context


_DESIGN_NOTES = """
# _exception_info_for_default

## Purpose
A specialized internal helper designed to unify metadata extraction across the default-value 
validation subsystem. By isolating the resolution of class names, parent boundaries, and 
context signatures, it ensures that all structural exception messages maintain a flawless, 
predictable layout without code duplication.

## Architecture & Integration
This component is treated as a private implementation detail of the validation engine. 
It directly serves and orchestrates the diagnostic payload for the following validation pillars:

1. `.../validations/composition/raise_default_is_defined_in_composition.py`
   - Intercepts scenarios where a structural compound object attempts to define a constant default.
2. `.../validations/constant/validate_default_is_defined.py`
   - Intercepts scenarios where a leaf constant structure completely omits its default definition.
3. `.../validations/constant/validate_default_matches_annotation.py`
   - Intercepts scenarios where the provided default breaks type-hint alignment.

## Resolution Logic
- **Attribute Target:** Fixed to `_default`, which represents the core framework parameter for constants.
- **Hierarchy Detection:** Inspects the Method Resolution Order (`__mro__`) of the target class. 
  If the target shares a lineage with `SimpleObject`, it flags the parent context accordingly; 
  otherwise, it falls back to a pure `SimpleConstant` operational context.
"""