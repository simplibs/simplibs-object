

__DOCT__ = """
## `attributes/descriptors/`

> **Subgroup purpose:**
> The descriptor protocols — the machinery underlying `property`, `classmethod`,
> `staticmethod`, and most ORMs. A *descriptor* is any object that defines `__get__`,
> `__set__`, or `__delete__` and is placed as a *class attribute* (not an instance
> attribute). Python's attribute lookup gives descriptors priority over the instance dict
> (data descriptors: define `__set__`; non-data descriptors: define only `__get__`).
"""