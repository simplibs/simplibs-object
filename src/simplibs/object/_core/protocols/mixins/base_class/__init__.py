from .SimpleMixinProtocol import SimpleMixinProtocol

# Element defining the largest set (superset for annotations)
SimpleMixinLike = SimpleMixinProtocol


_DESIGN_NOTES = """
# Mixin Base Class Protocols Sub-Package

## Purpose
Provides the foundational base protocol for all mixin classes across the framework.

## Internal Components Registry

| Component            | Type     | Description                                                                  |
| :------------------- | :------- | :--------------------------------------------------------------------------- |
| `SimpleMixinProtocol`| Protocol | Base anchor protocol guaranteeing identity and mixin initialization hooks.  |
"""
