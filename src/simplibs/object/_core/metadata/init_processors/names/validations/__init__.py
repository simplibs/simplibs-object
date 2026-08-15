from .validate_class_name_has_no_underscores import validate_class_name_has_no_underscores
from .validate_class_name_is_ascii import validate_class_name_is_ascii
from .validate_class_name_is_identifier import validate_class_name_is_identifier


_DESIGN_NOTES = """
# Class Name Validation Sub-Package

## Purpose
Houses specialized low-level validation filters designed to enforce strict lexical and structural constraints on class identifiers during the metadata extraction pipeline.

## Internal Components Registry

| Component                                | Type     | Description                                                                          |
| :--------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_class_name_is_identifier`      | Function | Ensures the identifier is a syntactically valid Python token, filtering out symbols. |
| `validate_class_name_is_ascii`           | Function | Strips out localized characters and diacritics, ensuring strict ASCII compliance.    |
| `validate_class_name_has_no_underscores` | Function | Rejects underscore characters, forcing a pure alphanumeric PascalCase blueprint.    |
"""