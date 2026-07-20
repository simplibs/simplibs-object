from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def exception_context_for_classmethod(
    bound_method: "ClassMethodProtocol",
) -> dict[str, str]:
    """Extracts essential identifying components from a bound classmethod into a standardized context dictionary."""

    # 1. Resolve class and functional block identifiers
    class_name = bound_method.__self__.__name__
    method_name = bound_method.__func__.__name__

    # 2. Formulate diagnostic context string
    context = f"Metadata evaluation and validation processing for: {class_name}.{method_name}"

    # 3. Yield structured data dictionary
    return {
        "class_name": class_name,
        "method_name": method_name,
        "context": context
    }


_DESIGN_NOTES = """
# exception_context_for_classmethod

## Purpose
Acts as a micro-utility providing minimal metadata extraction from a bound class method. It isolates 
identifying attributes (`class_name`, `method_name`) and constructs a standardized diagnostic context line.

## Rationale & Separation
Not all validation checks inside the method processing package require full blueprint formatting 
(which generates multi-line code examples). Simple verification checks—like checking if a method is 
callable or if it exists—only need basic contextual tracking. By separating this from the heavier 
structure generator, we avoid unnecessary string operations and keep error generation fast.

## Design Decisions
1. **Dictionary-Driven Pipeline**: Returns data via a structured dictionary mapping explicit keys 
   (`class_name`, `method_name`, `context`) to simplify downstream usage and prevent tracking order positional mistakes.
"""