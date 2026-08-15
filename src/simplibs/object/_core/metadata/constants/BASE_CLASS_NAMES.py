BASE_CLASS_NAMES = ("SimpleBase", "SimpleConstant", "SimpleObject")


_DESIGN_NOTES = """
# BASE_CLASS_NAMES

## Purpose
- Serves as a **stable identifier set** for all foundational Simple system classes.  
- Used to distinguish **system-level root classes** from **user-defined declarative blueprints**.  
- Ensures that base classes:
  - do **not** receive metadata,
  - cannot be instantiated,
  - are excluded from validation pipelines,
  - act purely as architectural anchors.

- Referenced in:
  - `calculate_blueprint_path.py` — base classes have no blueprint path.  
  - `validate_class_is_not_base_class.py` — prevents instantiation of base classes.  
  - `create_instance.py` — skips metadata and validation for base classes.  
  - `SimpleMeta.py` — decides whether metadata should be created for a class.

- This constant is intentionally **small, immutable, and stable**, because changing it would break the entire metadata lifecycle.
"""