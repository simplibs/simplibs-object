from .SimpleMixinMeta import SimpleMixinMeta

__all__ = ["SimpleMixinMeta"]

_DESIGN_NOTES = """
# Mixin Metaclass & Definition Validation Package

## Purpose
Provides the foundational metaclass (`SimpleMixinMeta`) and structural validation
pipeline responsible for verifying the correctness of mixin definitions in the Simple system.
Ensures that all mixins adhere to memory layout rules, declare proper compatibility flags,
isolate initialization hooks, and support runtime `isinstance` checks across flat-synthesized
instance classes.

## Internal Components Registry

| Component                   | Type       | Scope    | Description                                                              |
| :-------------------------- | :--------- | :------- | :----------------------------------------------------------------------- |
| `SimpleMixinMeta`           | Metaclass  | Public   | Base metaclass managing class-creation validation and `isinstance` checks.|
| `_verify_mixin_definition`  | Function   | Internal | Main validation pipeline executed during mixin subclass creation.        |
"""