from .SimpleMeta import SimpleMeta


_DESIGN_NOTES = """
# Metadata Sub-Package

## Purpose
Provides the core metaclass used to construct declarative Simple classes. Handles
metadata creation, write-once protection, and instance construction.

## Internal Components Registry

| Component     | Type       | Description                                      |
| :------------ | :--------- | :----------------------------------------------- |
| `SimpleMeta`  | Metaclass  | Central metaclass orchestrating metadata and instance creation. |
"""
