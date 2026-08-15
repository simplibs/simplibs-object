RESTRICTION_FLAGS = (
    "_constant_only",
    "_composite_only",
    "_mutable_only",
    "_immutable_only",
)

_DESIGN_NOTES = """
# RESTRICTION_FLAGS

## Purpose
Defines the complete set of declarative compatibility flags used by mixins to
express structural constraints on where they may be applied.

## Notes
Used by the mixin validation pipeline to ensure all declared flags are boolean.
Acts as a schema definition for mixin compatibility metadata.
"""
