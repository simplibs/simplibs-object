STEPPER = "_stepper"

_DESIGN_NOTES = """
# Constant Name Token

## Purpose
Represents a single, immutable string token used as an internal attribute
identifier within the Simple system. Serves as the sole source of truth for
the stepper attribute name, preventing accidental typos or shadowing.

## Notes
Changing this constant would break mixin attribute resolution and internal
object wiring. It is treated as a core invariant of the system.
"""
