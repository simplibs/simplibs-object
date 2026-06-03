from .ClassGetitem import ClassGetitemMixin

__all__ = (
    "ClassGetitemMixin",
)


__DOCT__ = """
## `lifecycle/class_hooks/`

> **Subgroup purpose:**
> Methods that fire at *class definition time*, not at instance creation time.
> These are the hooks Python provides so that creating or inheriting from a class
> can trigger custom logic — enabling patterns like automatic registration,
> generic type support, and descriptor naming.
"""