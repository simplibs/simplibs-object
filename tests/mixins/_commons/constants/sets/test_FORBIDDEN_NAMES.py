FORBIDDEN_NAMES = {
    "__init__",
    "__metadata__",
    "_decompose",
    "_inners",
    "_logic",
    "_owner",
    "_recalculate_inners",
    "_recalculate_self",
    "_value",
    "meta",
    "owner",
    "value",
}

_DESIGN_NOTES = """
# FORBIDDEN_NAMES

## Purpose
Defines a protected set of attribute names that must never appear inside mixin
definitions. These names are reserved for internal Simple system mechanics and
are critical for maintaining deterministic instance behavior.

## Notes
Used by the mixin validation pipeline to detect collisions in both `__slots__`
and class-level namespaces. Treated as a core invariant of the system.
"""
