

__DOCT__ = """
# GROUP: `attributes/`

> **Group purpose:**
> Everything related to *attribute access* — reading, writing, and deleting properties
> on an object. Python's attribute system is layered: it first checks the class hierarchy
> for data descriptors, then the instance `__dict__`, then non-data descriptors.
> The dunders in this group let you intercept any or all of those layers.
> This group also contains the descriptor protocols — the mechanism behind `property`,
> `classmethod`, `staticmethod`, and many ORMs.
"""